document.addEventListener("DOMContentLoaded", function () {
  // Debugging: Check if the script is running
  console.log("Script is running...");

  // Select all form labels
  const labels = document.querySelectorAll(".form label");

  // Debugging: Check if labels are selected
  console.log("Labels found: ", labels.length);

  // Check if labels exist before applying logic
  if (labels.length > 0) {
    labels.forEach((label) => {
      const input = label.querySelector("input");
      const span = label.querySelector("span");

      // Debugging: Log input and span elements
      console.log("Input and span found: ", input, span);

      if (input) {
        input.addEventListener("focus", () => {
          label.classList.add("focus");
          if (span) {
            span.style.top = "0";
          }
        });

        input.addEventListener("blur", () => {
          if (!input.value.trim()) {
            label.classList.remove("focus");
            if (span) {
              span.style.top = "50%";
            }
          }
        });
      }
    });
  }

  // Validation function
  function validateInputs() {
    // Debugging: Log that validation is running
    console.log("Validation running...");

    var radiusMean = parseFloat(document.getElementById("radius_mean").value);
    var perimeterMean = parseFloat(document.getElementById("perimeter_mean").value);
    var areaMean = parseFloat(document.getElementById("area_mean").value);
    var concavePointsMean = parseFloat(document.getElementById("concave_points_mean").value);
    var radiusWorst = parseFloat(document.getElementById("radius_worst").value);
    var perimeterWorst = parseFloat(document.getElementById("perimeter_worst").value);
    var areaWorst = parseFloat(document.getElementById("area_worst").value);
    var concavePointsWorst = parseFloat(document.getElementById("concave_points_worst").value);

    var valid = true;

    // Validate Radius Mean
    if (isNaN(radiusMean) || radiusMean < 6.981 || radiusMean > 28.11) {
      document.getElementById("radius_mean").style.borderColor = "red";
      valid = false;
    } else {
      document.getElementById("radius_mean").style.borderColor = "";
    }

    // Validate Perimeter Mean
    if (isNaN(perimeterMean) || perimeterMean < 43.79 || perimeterMean > 188.5) {
      document.getElementById("perimeter_mean").style.borderColor = "red";
      valid = false;
    } else {
      document.getElementById("perimeter_mean").style.borderColor = "";
    }

    // Validate Area Mean
    if (isNaN(areaMean) || areaMean < 143.5 || areaMean > 2501) {
      document.getElementById("area_mean").style.borderColor = "red";
      valid = false;
    } else {
      document.getElementById("area_mean").style.borderColor = "";
    }

    // Validate Concave Points Mean
    if (isNaN(concavePointsMean) || concavePointsMean < 0 || concavePointsMean > 0.2012) {
      document.getElementById("concave_points_mean").style.borderColor = "red";
      valid = false;
    } else {
      document.getElementById("concave_points_mean").style.borderColor = "";
    }

    // Validate Radius Worst
    if (isNaN(radiusWorst) || radiusWorst < 7.93 || radiusWorst > 36.04) {
      document.getElementById("radius_worst").style.borderColor = "red";
      valid = false;
    } else {
      document.getElementById("radius_worst").style.borderColor = "";
    }

    // Validate Perimeter Worst
    if (isNaN(perimeterWorst) || perimeterWorst < 50.41 || perimeterWorst > 251.2) {
      document.getElementById("perimeter_worst").style.borderColor = "red";
      valid = false;
    } else {
      document.getElementById("perimeter_worst").style.borderColor = "";
    }

    // Validate Area Worst
    if (isNaN(areaWorst) || areaWorst < 185.2 || areaWorst > 4254) {
      document.getElementById("area_worst").style.borderColor = "red";
      valid = false;
    } else {
      document.getElementById("area_worst").style.borderColor = "";
    }

    // Validate Concave Points Worst
    if (isNaN(concavePointsWorst) || concavePointsWorst < 0 || concavePointsWorst > 0.291) {
      document.getElementById("concave_points_worst").style.borderColor = "red";
      valid = false;
    } else {
      document.getElementById("concave_points_worst").style.borderColor = "";
    }

    if (!valid) {
      alert("Value must be within the range");
    }

    return valid;
  }

  // Get the form element
  var form = document.querySelector(".form");
  if (form) {
    form.onsubmit = function () {
      return validateInputs();
    };
  }

  
  
});
