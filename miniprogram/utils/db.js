const db = wx.cloud.database()
const _ = db.command

function getCollection(name) {
  return db.collection(name)
}

async function getById(collection, id) {
  const res = await db.collection(collection).doc(id).get()
  return res.data
}

async function queryList(collection, where, orderBy, limit = 20, skip = 0) {
  let query = db.collection(collection).where(where)
  if (orderBy) {
    query = query.orderBy(orderBy.field, orderBy.order || 'desc')
  }
  const res = await query.skip(skip).limit(limit).get()
  return res.data
}

async function addRecord(collection, data) {
  const res = await db.collection(collection).add({ data })
  return res._id
}

async function updateRecord(collection, id, data) {
  return db.collection(collection).doc(id).update({ data })
}

module.exports = { db, _, getCollection, getById, queryList, addRecord, updateRecord }
