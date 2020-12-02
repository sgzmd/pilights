function update_current_algo(algo, settings = null) {
    console.log("Setting algo to " + algo);
}

function update_speed(speed) {
    console.log("Setting speed to " + speed);
}

function refresh_all() {
    $.ajax({
        method: "POST",
        url: "/status"
    }).done(function(data) {
        console.log("Data refreshed: " + data);
        update_current_algo(data.current_algo, data.current_algo_settings);
        update_speed(data.speed);
    })
    .fail(function(){
        alert("Failed to refresh data");
    });
};