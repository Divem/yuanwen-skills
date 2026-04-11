function formatDate(date) {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function daysBetween(start, end) {
  const startDate = new Date(start)
  const endDate = new Date(end || Date.now())
  return Math.floor((endDate - startDate) / (1000 * 60 * 60 * 24))
}

function generateAdoptionCode() {
  const now = new Date()
  const dateStr = formatDate(now).replace(/-/g, '')
  const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
  return `ZD-${dateStr}-${random}`
}

module.exports = { formatDate, daysBetween, generateAdoptionCode }
