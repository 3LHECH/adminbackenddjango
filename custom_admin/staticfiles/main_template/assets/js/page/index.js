"use strict";

function chart1() {
    fetch("http://127.0.0.1:8000/user/api/user-signups/")
        .then(response => response.json())
        .then(data => {
            // Transformation des données API en format graphique
            // Convertir la date ISO en format lisible pour l'axe X
            const categories = data.map(item => new Date(item.month).toLocaleDateString());
            // Nombre d'inscriptions pour chaque mois
            const counts = data.map(item => item.count);

            const options = {
                chart: {
                    height: 230,
                    type: "line",
                    toolbar: { show: false }
                },
                colors: ["#786BED"],
                dataLabels: { enabled: true },
                stroke: { curve: "smooth" },
                series: [{
                    name: "User Signups",
                    data: counts
                }],
                xaxis: {
                    categories: categories,
                    labels: { style: { colors: "#9aa0ac" } }
                },
                yaxis: {
                    title: { text: "Signups" },
                    labels: { style: { color: "#9aa0ac" } },
                    min: 0
                },
                grid: { borderColor: "#e7e7e7" }
            };

            var chart = new ApexCharts(document.querySelector("#chart1"), options);
            chart.render();
        })
        .catch(error => {
            console.error("Error loading chart data:", error);
        });
}

// Lancer le graphique au chargement de la page
document.addEventListener("DOMContentLoaded", chart1);
