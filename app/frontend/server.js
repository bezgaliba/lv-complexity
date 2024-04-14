const express = require('express');
const path = require('path');
const app = express();

// Middleware to enable CORS
app.use((req, res, next) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

// connection to front end
app.use(express.static(path.join(__dirname, 'build')));

// API endpoint
app.get('/api/decapri/:id', (req, res) => {
    const id = req.params.id;
    const sarezgitiba = getSarezgitiba(id);
    if (!sarezgitiba) {
        res.status(404).send({error: `Sarezgitiba ${id} not found.`})
    }
    else {
        res.send({ data: sarezgitiba})
    }
})

function getSarezgitiba(id) {
    const sarezgitiba = [
        { id: 1, string: 'PirmaSarezgitiba', code: '152' },
        { id: 2, string: 'OtraSarezgitiba', code: '481238' },
        { id: 3, string: 'TresaSarezgitiba', code: '634523'},
    ]
    return sarezgitiba.find(p => p.id == id);
}

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
