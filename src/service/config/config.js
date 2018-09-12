var httpStatusSuccess = 200
var httpStatusBadrequest = 400
var httpStatusForbidden = 404
var httpStatusFailure = 420
var httpStatusServererror = 500

function submitCode() {
    //
    var config = {"categories": [], "country": "", "language": "", "sources": []}
    //
    var inptCategories = document.getElementsByName("category");
    for (var category in inptCategories) {
        if (inptCategories[category].checked) {
            config.categories.push(inptCategories[category].id);
        }
    }
    var inptCountries = document.getElementsByName("country");
    for (var country in inptCountries) {
        if (inptCountries[country].checked) {
            config.country = inptCountries[country].id;
            break;
        }
    }
    var inptLanguages = document.getElementsByName("language");
    for (var language in inptLanguages) {
        if (inptLanguages[language].checked) {
            config.language = inptLanguages[language].id;
            break;
        }
    }
    var inptSources = document.getElementsByName("source");
    for (var source in inptSources) {
        if (inptSources[source].checked) {
            config.sources.push(inptSources[source].id);
        }
    }
    //
    httpGetAsync("/news/config/update", "POST", config, submitCode_callback);
}
function submitCode_callback(result, response={}) {
    if (result==httpStatusSuccess) {
        document.getElementById("alert_submit").className = "alert alert-success";
        document.getElementById("alert_submit").innerHTML = "Code requested";
    } else if (result==httpStatusFailure) {
        document.getElementById("alert_submit").className = "alert alert-warning";
        document.getElementById("alert_submit").innerHTML = response.error;
    } else {
        document.getElementById("alert_submit").className = "alert alert-danger";
        document.getElementById("alert_submit").innerHTML = "An error has occurred, please try again.";
    }
    document.getElementById("alert_submit").style.visibility = "inherit";
}

function httpGetAsync(theUri, method, body, callback) {
    //
    //var service_header_clientid_label = "jarvis.client-service";
    //var service_id = "news_config";
    //
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == httpStatusSuccess) {
                // operation success
                callback(httpStatusSuccess);
            } else if (xmlHttp.status == httpStatusFailure) {
                // operation failure
                callback(httpStatusFailure, JSON.parse(xmlHttp.responseText));
            } else if (xmlHttp.status == httpStatusBadrequest ||
                        xmlHttp.status == httpStatusForbidden ||
                        xmlHttp.status == httpStatusServererror) {
                // failures such as forbidden, server error, etc.
                callback(false);
            }
         }
    }
    xmlHttp.open(method, theUri, true); // true for asynchronous
    xmlHttp.setRequestHeader("Content-Type", "application/json");
    //xmlHttp.setRequestHeader(service_header_clientid_label, service_id);
    if (body) {
        xmlHttp.send(JSON.stringify(body));
    } else {
        xmlHttp.send(null);
    }
    //
}
