// back end

const express = require('express');
const path = require('path');
const app = express();

// connection to front end
app.use(express.static(path.join(__dirname, 'build')));

// API endpoint
app.get('/api/sarezgitiba/:id', (req, res) => {
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

const port = process.env.PORT || 8080;
app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
