const express = require('express')
const cors = require('cors')
const sqlite3 = require('sqlite3').verbose()
const app = express()

app.use(cors())
app.use(express.json())

const db = new sqlite3.Database('./tournaments.db')

db.run(`
  CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    fields INTEGER,
    breakLength INTEGER,
    matchTime INTEGER,
    startTime TEXT,
    mode TEXT
  )
`)

app.post('/api/tournaments', (req, res) => {
  const { name, fields, breakLength, matchTime, startTime, mode } = req.body

  db.run(
    `INSERT INTO tournaments (name, fields, breakLength, matchTime, startTime, mode)
     VALUES (?, ?, ?, ?, ?, ?)`,
    [name, fields, breakLength, matchTime, startTime, mode],
    function (err) {
      if (err) {
        return res.status(500).json({ error: err.message })
      }
      res.json({ id: this.lastID })
    }
  )
})

app.listen(3000, () => {
  console.log('✅ Backend läuft auf http://localhost:3000')
})
