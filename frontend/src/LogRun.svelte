<script>
    import { onMount } from "svelte";
    import { distanceUnitStore } from "./stores.js";

    let date = new Date().toISOString().slice(0, 10),
        distance = 0.0,
        duration_mins = 0.0,
        comments = "",
        errors = {},
        distanceUnit;

    distanceUnitStore.subscribe((value) => {
        distanceUnit = value;
    });

    function isValidInput() {
        let valid = true;
        errors = {};

        if (!date) {
            errors.date = "Date was undefined";
            valid = false;
        }

        if (isNaN(distance)) {
            errors.distance = "Distance was undefined";
            valid = false;
        } else if (distance <= 0.0) {
            errors.distance = "Distance must be > 0 " + distanceUnit;
            valid = false;
        }

        if (isNaN(duration_mins)) {
            errors.duration_mins = "Duration was undefined";
            valid = false;
        } else if (duration_mins <= 0.0) {
            errors.duration_mins = "Duration must be > 0 minutes";
            valid = false;
        }
        return valid;
    }

    function logRun() {
        // convert to distance in miles for storage
        let parsedDistance = parseFloat(distance),
            distanceMiles =
                distanceUnit === "miles"
                    ? parsedDistance
                    : parsedDistance / 1.609;

        let run = {
            date: date,
            distance_miles: distanceMiles.toFixed(2),
            duration_mins: parseFloat(duration_mins).toFixed(2),
            comments: comments,
        };
        fetch("http://localhost:8080/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(run),
        }).then(function (response) {
            if (response.status == 409) {
                response.json().then((body) => {
                    alert(body.detail);
                });
            } else {
                location.reload();
            }
        });
    }

    const handleSubmit = () => {
        if (isValidInput()) {
            errors = {};
            logRun();
        }
    };

    onMount(async () => {
        document.getElementById("log-run-date").valueAsDate = new Date(date);
        distanceUnitStore.useLocalStorage();
    });
</script>

<div class="container">
    <form on:submit|preventDefault={handleSubmit}>
        <div class="row">
            <div class="col-25">
                <label for="log-run-date">Date:</label>
            </div>
            <div class="col-75">
                <input type="date" id="log-run-date" bind:value={date} />
                {#if errors.date}
                    <span class="error">{errors.date}</span>
                {/if}
            </div>
        </div>

        <div class="row">
            <div class="col-25">
                <label for="log-run-distance">Distance ({distanceUnit}):</label>
            </div>
            <div class="col-75">
                <input
                    type="text"
                    id="log-run-distance"
                    bind:value={distance}
                    placeholder="0.0"
                />
                {#if errors.distance}
                    <span class="error">{errors.distance}</span>
                {/if}
            </div>
        </div>

        <div class="row">
            <div class="col-25">
                <label for="log-run-duration">Duration (minutes):</label>
            </div>
            <div class="col-75">
                <input
                    type="text"
                    id="log-run-duration"
                    bind:value={duration_mins}
                    placeholder="0.0"
                />
                {#if errors.duration_mins}
                    <span class="error">{errors.duration_mins}</span>
                {/if}
            </div>
        </div>

        <div class="row">
            <div class="col-25">
                <label for="log-run-comments">Comments:</label>
            </div>
            <div class="col-75">
                <textarea id="log-run-comments" bind:value={comments} />
            </div>
        </div>

        <div class="row">
            <input type="submit" />
        </div>
    </form>
</div>

<style>
    * {
        box-sizing: border-box;
    }

    .error {
        color: #ff3e00;
        font-size: 1em;
        font-weight: 500;
    }

    input[type="text"],
    textarea {
        width: 100%;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
        resize: vertical;
    }

    label {
        padding: 12px 12px 12px 0;
        display: inline-block;
    }

    input[type="submit"] {
        background-color: #ff3e00;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        float: right;
    }

    input[type="submit"]:hover {
        background-color: #fa8761;
    }

    .container {
        border-radius: 5px;
        background-color: #f2f2f2;
        padding: 20px;
    }

    .col-25 {
        float: left;
        width: 25%;
        margin-top: 6px;
    }

    .col-75 {
        float: left;
        width: 75%;
        margin-top: 6px;
    }

    /* Clear floats after the columns */
    .row:after {
        content: "";
        display: table;
        clear: both;
    }

    /* Responsive layout - when the screen is less than 600px wide, make the two columns stack on top of each other instead of next to each other */
    @media screen and (max-width: 600px) {
        .col-25,
        .col-75,
        input[type="submit"] {
            width: 100%;
            margin-top: 0;
        }
    }
</style>
