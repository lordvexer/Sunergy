// Tabs
function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    $('#' + cityName).parent().find('.tabcontent').removeClass('active').css('display', 'none');
    $('#' + cityName).parent().find('.tablinks').removeClass('active');
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}


// Modal 1
document.getElementById('solarCalcForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent page reload

    const capacity = document.getElementById('capacity').value;
    
    // Validate input
    if (isNaN(capacity) || capacity <= 0) {
        alert('Please enter a valid capacity greater than zero.');
        return;
    }

    // Show loading indicator
    const resultElement = document.getElementById('result');
    resultElement.innerHTML = 'Calculating...';

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `capacity=${capacity}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        resultElement.innerHTML = `
            <p>فضای مورد نیاز اجرا روی زمین: ${data.ground_space} متر مربع</p>
            <p>فضای مورد نیاز اجرا روی سقف: ${data.rooftop_space} متر مربع</p>
            <p>هزینه احداث: ${data.construction_cost.toLocaleString()} تومان</p>
            <p>${data.roi_message}</p>
        `;
    })
    .catch(error => {
        resultElement.innerHTML = 'An error occurred: ' + error.message;
        console.error('Error:', error);
    });
});


// Modal2
document.getElementById("calculateButton").addEventListener("click", function () {
    const energy = parseFloat(document.getElementById("annualEnergy").value);
    const errorMessage = document.getElementById("errorMessage");
    const capacityOutput = document.getElementById("capacityOutput");

    if (isNaN(energy) || energy <= 1000) {
        errorMessage.style.display = "block"; // نمایش پیام خطا
        capacityOutput.textContent = ""; // پاک کردن مقدار قبلی
    } else {
        errorMessage.style.display = "none"; // مخفی کردن پیام خطا
        
        fetch(`/calculate_capacity?energy=${energy}`)
            .then(response => response.json())
            .then(data => {
                if (data.capacity !== undefined) {
                    capacityOutput.textContent = data.capacity;
                } else {
                    capacityOutput.textContent = "خطا در محاسبه";
                }
            })
            .catch(error => {
                capacityOutput.textContent = "مشکلی در ارتباط با سرور پیش آمد";
            });
    }
});

// Loading
setTimeout(() => {
    document.getElementById('fullscreen-modal').style.display = 'none';
    document.getElementById('main-content').style.display = 'block';
}, 4000);