<script>
    import { onMount } from "svelte";
    import {
        Chart,
        ArcElement,
        LineElement,
        BarElement,
        PointElement,
        BarController,
        BubbleController,
        DoughnutController,
        LineController,
        PieController,
        PolarAreaController,
        RadarController,
        ScatterController,
        CategoryScale,
        LinearScale,
        LogarithmicScale,
        RadialLinearScale,
        TimeScale,
        TimeSeriesScale,
        Decimation,
        Filler,
        Legend,
        Title,
        Tooltip,
        SubTitle,
    } from "chart.js";

    Chart.register(
        ArcElement,
        LineElement,
        BarElement,
        PointElement,
        BarController,
        BubbleController,
        DoughnutController,
        LineController,
        PieController,
        PolarAreaController,
        RadarController,
        ScatterController,
        CategoryScale,
        LinearScale,
        LogarithmicScale,
        RadialLinearScale,
        TimeScale,
        TimeSeriesScale,
        Decimation,
        Filler,
        Legend,
        Title,
        Tooltip,
        SubTitle
    );

    import "chartjs-adapter-date-fns";
    import { distanceUnitStore } from "./stores.js";

    let startDate = "2017-01-01",
        endDate = new Date().toISOString().slice(0, 10),
        timeUnit = "weekly",
        distanceUnit;
    var mileageChart;

    distanceUnitStore.subscribe((value) => {
        distanceUnit = value;
    });

    const buildDataUrl = () => {
        var url = "http://localhost:8080/runs?";
        url += "time_unit=" + timeUnit;
        if (startDate) {
            url += "&start_date=" + startDate;
        }
        if (endDate) {
            url += "&end_date=" + endDate;
        }
        return url;
    };

    const showData = async () => {
        try {
            mileageChart.destroy();
        } catch (err) {}

        let xAxisLabel = timeUnit == "weekly" ? "Per week" : "Per Month";

        const response = await fetch(buildDataUrl());
        let timeSeries = await response.json();

        if (distanceUnit === "km") {
            timeSeries.forEach((d) => (d.y *= 1.609));
        }

        const data = {
            datasets: [
                {
                    borderColor: "#ff3e00",
                    backgroundColor: "#ff3e00",
                    data: timeSeries,
                },
            ],
        };

        const config = {
            type: "line",
            data: data,
            options: {
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: "Distance (" + distanceUnit + ")",
                        },
                    },
                    x: {
                        title: {
                            display: true,
                            text: xAxisLabel,
                        },
                        type: "timeseries",
                        time: {
                            unit: "month",
                            tooltipFormat: "yyyy-MM-dd",
                        },
                    },
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                },
            },
        };

        mileageChart = new Chart(
            document.getElementById("mileage-chart"),
            config
        );
    };

    onMount(async () => {
        document.getElementById("chart-start-date").valueAsDate = new Date(
            startDate
        );
        document.getElementById("chart-end-date").valueAsDate = new Date(
            endDate
        );
        distanceUnitStore.useLocalStorage();
    });
</script>

<div>
    <div>
        <label for="chart-start-date">Start date:</label>
        <input type="date" id="chart-start-date" bind:value={startDate} />

        <label for="chart-end-date">End date:</label>
        <input type="date" id="chart-end-date" bind:value={endDate} />

        <label for="chart-time-aggregation">Time unit:</label>
        <select id="chart-time-aggregation" bind:value={timeUnit}>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
        </select>

        <button id="show-data" on:click={showData}>Show</button>
    </div>
    <canvas id="mileage-chart" />
</div>

<style>
    input,
    label {
        display: inline;
    }

    #show-data {
        background-color: #ff3e00;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    #show-data:hover {
        background-color: #fa8761;
    }
</style>
