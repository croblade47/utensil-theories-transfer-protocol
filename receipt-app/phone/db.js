// Tiny IndexedDB wrapper. All data lives on the phone until synced.
const DB = (() => {
  const NAME = 'door-receipts';
  const VERSION = 1;
  let dbp;

  function open() {
    if (dbp) return dbp;
    dbp = new Promise((resolve, reject) => {
      const req = indexedDB.open(NAME, VERSION);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains('visits')) {
          const s = db.createObjectStore('visits', { keyPath: 'id' });
          s.createIndex('shiftId', 'shiftId');
        }
        if (!db.objectStoreNames.contains('shifts')) db.createObjectStore('shifts', { keyPath: 'id' });
        if (!db.objectStoreNames.contains('points')) {
          const p = db.createObjectStore('points', { keyPath: 'key', autoIncrement: true });
          p.createIndex('shiftId', 'shiftId');
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
    return dbp;
  }

  async function tx(store, mode, fn) {
    const db = await open();
    return new Promise((resolve, reject) => {
      const t = db.transaction(store, mode);
      const s = t.objectStore(store);
      let out;
      Promise.resolve(fn(s)).then(v => { out = v; });
      t.oncomplete = () => resolve(out);
      t.onerror = () => reject(t.error);
    });
  }

  const reqP = r => new Promise((res, rej) => { r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });

  return {
    put: (store, obj) => tx(store, 'readwrite', s => reqP(s.put(obj))),
    get: (store, key) => tx(store, 'readonly', s => reqP(s.get(key))),
    del: (store, key) => tx(store, 'readwrite', s => reqP(s.delete(key))),
    all: (store) => tx(store, 'readonly', s => reqP(s.getAll())),
    byShift: (store, shiftId) => tx(store, 'readonly', s => reqP(s.index('shiftId').getAll(shiftId))),
  };
})();
