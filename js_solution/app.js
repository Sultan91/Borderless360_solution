var express = require('express');
var app = express();
let ejs = require('ejs');
app.set('view engine', 'ejs');
app.get('/', function(req, res) {
    let data = require('../data/sample2.json');
    let results = OrderHistory(data['results'])
    res.render('index.ejs', {results: results});

});

app.listen(8080);
console.log('8080 is the magic port');


// ----------------------------------   OrderHistory
function dict_diff(dict1, dict2){
    let diffs = new Map()
    if (dict1 === null || dict1 ===undefined) {
        return diffs
    }
    else {
        let all_keys = Object.keys(dict1)
        for (let k of all_keys) {
            if (typeof dict1[k] === "object") {
                let temp = dict_diff(dict1[k], dict2[k])
                if (temp.size > 0) {
                    diffs[k] = temp
                }
            } else if (dict1[k] !== dict2[k]) {
                diffs.set(k, [dict1[k], dict2[k]])
            }
        }
        return diffs
    }
}

function OrderHistory(data_results) {
    let outputs = []
    for (let i=data_results.length-1; i>1 ; i--){
        let res = dict_diff(data_results[i]['model_data'], data_results[i-1]['model_data'])
        if(res.get('fulfillments')!==undefined){
            let fulfill_temp = dict_diff(res.get('fulfillments')[0][0], res.get('fulfillments')[1][0])
            console.log(fulfill_temp)
        }
        let username = data_results[i]['user']
        if (username == null || username === '')
        {
            username = 'System'
        }
        else {
            username = data_results[i]['user']['username']
        }
        let output_str = username
        output_str += ", NEW ACTION"
        if (data_results[i]['event_type']==='updated'){
            output_str += ", ORDER UPDATED"
        }
        output_str += ": "+data_results[i]['model_data']['status_display']
        outputs.push(output_str)
    }
    return outputs.reverse();
}



