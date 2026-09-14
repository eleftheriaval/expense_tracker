function selectChart(selected){
    if (selected === "categoryChart"){
        document.getElementById("monthlyBarChart").style.display = "none";
        document.getElementById("yearlyBarChart").style.display = "none";
        document.getElementById("selectYear").style.display= "none";
        document.getElementById("categoryPieChart").style.display = "block";
        loadCategoryPieChart()
    }
    if (selected === "monthlyChart"){
        document.getElementById("yearlyBarChart").style.display = "none";
        document.getElementById("categoryPieChart").style.display = "none";
        document.getElementById("selectYear").style.display= "block";
        saved_years();
    }
    if (selected === "yearlyChart"){
        document.getElementById("categoryPieChart").style.display = "none";
        document.getElementById("monthlyBarChart").style.display = "none";
        document.getElementById("selectYear").style.display= "none";
        document.getElementById("yearlyBarChart").style.display = "block";
        loadYearlyBarChart()
    }
}

let categoryPieChart = null;

function loadCategoryPieChart() {
    fetch("/user_home/charts")
    .then(response => {
        if (!response.ok) {
            throw new Error('Σφάλμα HTTP: ' + response.status);
        }
        return response.json();
    })
    .then(results => {
        if (categoryPieChart) {
            categoryPieChart.destroy();
        }

        const labels = [];
        const values = [];

        results.forEach(result => {
            labels.push(result[0]);
            values.push(result[1]);
        });

        const categoryPieChartData = {
            labels: labels,
            datasets: [{
                label: 'Expenses by category (€)',
                data: values,
                backgroundColor: [
                    '#e49cb9',
                    '#c8a6c8',
                    '#a3c2cd',
                    '#f4e598',
                    '#abe4c0',
                    '#add6fa',
                    '#c9c9e8',
                    '#faf7c5',
                    '#ccc6c6'
                ],
                hoverOffset: 5
            }]
        };

        const categoryChart = document.getElementById("categoryPieChart");
        categoryPieChart = new Chart(categoryChart, {
            type: 'pie',
            data: categoryPieChartData
        });
    });
}


let yearlyBarChart = null;

function loadYearlyBarChart() {
    fetch("/user_home/charts_yearly")
    .then(response => {
        if (!response.ok) {
            throw new Error('Σφάλμα HTTP: ' + response.status);
        }
        return response.json();
    })
    .then(results => {
        if (yearlyBarChart) {
            yearlyBarChart.destroy();
        }

        const labels = [];
        const values = [];

        results.forEach(result => {
            labels.push(result[0]);
            values.push(result[1]);
        });

        const yearlyBarChartData = {
            labels: labels,
            datasets: [{
                label: 'Expenses by year (€)',
                data: values,
                backgroundColor: [
                    '#e49cb9',
                    '#c8a6c8',
                    '#a3c2cd',
                    '#f4e598',
                    '#abe4c0',
                    '#add6fa',
                    '#c9c9e8',
                    '#faf7c5',
                    '#ccc6c6'
                ]
            }]
        };

        const yearlyChart = document.getElementById("yearlyBarChart");
        yearlyBarChart = new Chart(yearlyChart, {
            type: 'bar',
            data: yearlyBarChartData
        });
    });
}


let monthlyBarChart = null;

function loadMonthlyBarChart(year) {
    fetch("/user_home/charts_monthly?year=" + year)
    .then(response => {
        if (!response.ok) {
            throw new Error('Σφάλμα HTTP: ' + response.status);
        }
        return response.json();
    })
    .then(results => {
        if (monthlyBarChart) {
            monthlyBarChart.destroy();
        }

        document.getElementById("monthlyBarChart").style.display = "block";

        const labels = [];
        const values = [];

        results.forEach(result => {
            labels.push(result[0]);
            values.push(result[1]);
        });

        const monthlyBarChartData = {
            labels: labels,
            datasets: [{
                label: 'Expenses by month (€)',
                data: values,
                backgroundColor: [
                    '#e49cb9',
                    '#c8a6c8',
                    '#a3c2cd',
                    '#f4e598',
                    '#abe4c0',
                    '#add6fa',
                    '#c9c9e8',
                    '#faf7c5',
                    '#ccc6c6'
                ]
            }]
        };

        const monthlyChart = document.getElementById("monthlyBarChart");
        monthlyBarChart = new Chart(monthlyChart, {
            type: 'bar',
            data: monthlyBarChartData
        });
    });
}


function saved_years() {
    fetch("/user_home/years")
    .then(response => {
        if (!response.ok) {
            throw new Error('Σφάλμα HTTP: ' + response.status);
        }
        return response.json();
    })
    .then(results => {
        document.getElementById("selectYear").innerHTML = '';
        const start_option = document.createElement("option")
        start_option.textContent = "Select year"
        start_option.value = ""
        start_option.selected = true;
        start_option.disabled = true;
        document.getElementById("selectYear").appendChild(start_option)

        results.forEach(result => {
            const option = document.createElement("option")
            option.textContent = result[0]
            option.value = result [0]
            document.getElementById("selectYear").appendChild(option)
        });
    });
}