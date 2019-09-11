let request = require('request');
let cheerio = require('cheerio');
const fs = require('fs');

const DAY = 86400000;
const BUFFER_SIZE = 10;
let writing = false;
let queue_list = [];
let mesi = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
    'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
let startDate = new Date(1199145600000 + DAY);

function parse(date) {
    let strDate = ('0' + date.getDate()).slice(-2) + '-'
        + ('0' + (date.getMonth() + 1)).slice(-2) + '-'
        + date.getFullYear();
    let urlGet = mesi[date.getMonth()] + '-' + date.getUTCFullYear() + '/' + strDate + '.html';
    request('https://oroscopo.grazia.it/archivio/oroscopo-del-giorno/' + urlGet, {}, (err, res, body) => {
        if (err) {
            return console.log(err);
        }
        const $ = cheerio.load(body);
        let text = strDate + '\n';
        $('.main > .box ').each(function (index, element) {
            text += $(this).find('h3').text().trim() + '\n';
            text += $(this).find('.row').text().trim() + '\n';
            text += '\n';
        });
        queue(date, text)
    });
}

function queue(date, text){
    let i;
    for(i = 0; i < queue_list.length; i += 1){
        if (queue_list[i].date > date){
            break;
        }
    }
    queue_list.splice(i, 0, {'date': date, 'text': text});
    write();
}

function write() {
    if (queue_list.length > BUFFER_SIZE && !writing) {
        writing = true;
        let element = queue_list.shift();
        fs.appendFile('input.txt', element.text, function (err) {
            if (err) throw err;
            console.log('Saved ' + element.date);
            writing = false;
            write();
        });
    }
}

function run() {
    setTimeout(function () {
        let day = new Date(startDate.getTime() + i * DAY);
        parse(day);
        i += 1;
        if (day < new Date()){
            run();
        }
    }, 300);
}

let i = 0;
run();