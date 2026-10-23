import unittest

from resonance_engine import (
    Category,
    ContextualResonanceEngine,
    EngineConfig,
    HumanErrorEncoder,
)


class EncoderTests(unittest.TestCase):
    def setUp(self):
        self.enc = HumanErrorEncoder()

    def test_neutral_text_scores_zero(self):
        m = self.enc.encode_error("Planning a garden this weekend.")
        self.assertEqual(m["deviation_index"], 0.0)
        self.assertFalse(m["requires_grace"])
        self.assertEqual(m["errors_detected"], [])

    def test_word_forms_match(self):
        for text in ["I made mistakes", "I am hiding", "I was failing", "they betrayed us", "my sins"]:
            self.assertGreater(self.enc.encode_error(text)["deviation_index"], 0, text)

    def test_no_partial_word_matches(self):
        # "sin" must not fire inside "single", "business" or "casino"
        self.assertEqual(self.enc.encode_error("single business casino")["deviation_index"], 0.0)

    def test_negation_is_ignored(self):
        m = self.enc.encode_error("I have no guilt and I don't regret it.")
        self.assertEqual(m["deviation_index"], 0.0)
        self.assertEqual(sorted(m["negated_terms"]), ["guilt", "regret"])

    def test_negation_does_not_cross_clauses(self):
        m = self.enc.encode_error("Not today, but the guilt is heavy.")
        self.assertIn("regret", m["errors_detected"])

    def test_single_light_word_is_not_grace(self):
        m = self.enc.encode_error("I made a mistake.")
        self.assertGreater(m["deviation_index"], 0)
        self.assertFalse(m["requires_grace"])

    def test_index_stays_in_range_and_does_not_pin(self):
        heavy = self.enc.encode_error(
            "I hide behind this wall I built from fear. I failed to protect the secret, and the guilt is heavy.")
        self.assertTrue(0 < heavy["deviation_index"] < 1)
        self.assertTrue(heavy["requires_grace"])

    def test_more_weight_scores_higher(self):
        light = self.enc.encode_error("I made a mistake.")["deviation_index"]
        heavier = self.enc.encode_error("I made a mistake and I hide the secret.")["deviation_index"]
        self.assertGreater(heavier, light)

    def test_evidence_is_ordered_by_position(self):
        m = self.enc.encode_error("secret then guilt")
        self.assertEqual([e["term"] for e in m["evidence"]], ["secret", "guilt"])

    def test_bad_config_rejected(self):
        with self.assertRaises(ValueError):
            EngineConfig(triggers={"oops": "missing_category"})

    def test_custom_config(self):
        cfg = EngineConfig(categories={"joy": Category(0.9, "bright")}, triggers={r"happy": "joy"})
        m = HumanErrorEncoder(cfg).encode_error("so happy")
        self.assertEqual(m["resonance_shift"], "bright")


class EngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = ContextualResonanceEngine()

    def stance(self, text):
        return self.engine.process_input(text)["subconscious_translation"]["stance"]

    def test_all_stances_reachable(self):
        E = ContextualResonanceEngine
        self.assertEqual(self.stance("Nice weather."), E.STANCE_NEUTRAL)
        self.assertEqual(self.stance("I made a mistake."), E.STANCE_CORRECTION)
        self.assertEqual(self.stance("The guilt is heavy and I hide it."), E.STANCE_ATLAS)
        self.assertEqual(self.stance("He betrayed me."), E.STANCE_HALT)

    def test_wavelength_is_deterministic(self):
        a = self.engine.process_input("The guilt is heavy")
        b = self.engine.process_input("the   GUILT is heavy")
        self.assertEqual(a["subconscious_translation"]["resonance_wavelength"],
                         b["subconscious_translation"]["resonance_wavelength"])

    def test_salt_changes_wavelength(self):
        salted = ContextualResonanceEngine(EngineConfig(hash_salt="x"))
        self.assertNotEqual(
            self.engine.process_input("guilt")["subconscious_translation"]["resonance_wavelength"],
            salted.process_input("guilt")["subconscious_translation"]["resonance_wavelength"])

    def test_echo_input_can_be_disabled(self):
        quiet = ContextualResonanceEngine(EngineConfig(echo_input=False))
        self.assertNotIn("input_received", quiet.process_input("secret"))
        self.assertIn("input_received", self.engine.process_input("secret"))

    def test_non_string_rejected(self):
        with self.assertRaises(TypeError):
            self.engine.process_input(None)


if __name__ == "__main__":
    unittest.main()
