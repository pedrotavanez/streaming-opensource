//Currently working
function headers_to_json(r) {
  return JSON.stringify(r.headersIn)
}


function headers_to_json_not_working(r) {
    var kvpairs = JSON.stringify(r);
    for (var h in r.headers) {
        if ( kvpairs.length ) {
            kvpairs += ',';
        }
        kvpairs += '"' + h + '":';
        if ( isNaN(r.headers[h]) ) {
            kvpairs += '"' + r.headers[h] + '"';
        } else {
            kvpairs += r.headers[h];
        }
    }
    return kvpairs;
}
export default {headers_to_json};