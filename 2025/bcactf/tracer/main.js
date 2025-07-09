const express = require('express')
const { resolve } = require('path')
const { readFileSync } = require('fs')

const flag = readFileSync('flag.txt', 'utf-8')

const app = express()

app.use(express.urlencoded({ extended: true }))

app.get('/', (_req, res) => {
    res.sendFile(resolve('index.html'))
})

const caseInsensitiveCompare = (a, b) => {
    // console.log('Comparing:', a, b);
    console.log("Lengths:", a.length, b.length);
    console.log("First characters:", a[0].toLowerCase(), b[0].toLowerCase());
    if (!a.length && !b.length) {
        return true
    } else if (a.length !== b.length || a[0].toLowerCase() !== b[0].toLowerCase()) {
        return false
    }

    return caseInsensitiveCompare(a.slice(1), b.slice(1))
}

app.post('/', (req, res) => {
    // console.log(JSON.stringify(req.body.value));
    // console.log('length:', req.body?.value?.length);
    if (req.body?.value?.length > 100) {
        res.status(400).send('Bad Request')
        return
    }

    console.log(JSON.stringify(req.body.value));
    if (caseInsensitiveCompare(flag, req.body.value)) {
        res.status(200).send('Correct')
    } else {
        res.status(200).send('Incorrect')
    }
})

process.on('uncaughtException', err => {
    console.error(err)
})

app.listen(3000, console.log('Up on port 3000'))
