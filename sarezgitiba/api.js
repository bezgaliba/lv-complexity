const express = require('express');
const app = express();
app.use(express.json());
app.use(express.static('sarezgitiba/build'));
const port = process.env.PORT || 8080;
app.listen(port, () => {
    console.log(`Listening on port ${port}`);
})

app.get('/api/sarezgitiba/:id', (req, res) => {
    const id = req.params.id;
    const sarezgitiba = getSarezgitiba(id);
    if (!sarezgitiba) {
        res.status(404).send({error: `Sarezgitia ${id} not found.`})
    }
    else {
        res.send({ data: sarezgitiba})
    }
})

function getSarezgitiba(id) {
    const sarezgitiba = [
        { id: 1, string: 'PirmaSarezgitiba', code: '152' },
        { id: 2, string: 'Oraarezgitiba', code: '481238' },
        { id: 3, string: 'TresaSarezgitiba', code: '634523'},
    ]
    return sarezgitiba.find(p => p.id == id);
}