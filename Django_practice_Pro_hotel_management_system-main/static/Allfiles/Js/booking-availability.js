/**
 * Dostępność pokoi — ukrywa pełne typy, blokuje zajęte daty.
 */
(function () {
  var form = document.getElementById("booking-form");
  if (!form) return;

  var roomSelector = document.getElementById("room-selector");
  var checkInInput = document.getElementById("check-in-date");
  var checkOutInput = document.getElementById("check-out-date");
  var availHint = document.getElementById("availability-hint");
  var apiUrl = form.getAttribute("data-availability-url");
  if (!roomSelector || !checkInInput || !checkOutInput || !apiUrl) return;

  var blockedCheckin = [];
  var blockedCheckout = [];
  var fetchTimer = null;

  function showHint(msg, isError) {
    if (!availHint) return;
    availHint.textContent = msg || "";
    availHint.className = "booking-avail-hint" + (isError ? " is-error" : msg ? " is-info" : "");
  }

  function fetchAvailability() {
    var params = new URLSearchParams();
    if (checkInInput.value) params.set("check_in", checkInInput.value);
    if (checkOutInput.value) params.set("check_out", checkOutInput.value);
    var rt = roomSelector.value;
    if (rt) params.set("room_type", rt);

    return fetch(apiUrl + "?" + params.toString(), {
      headers: { Accept: "application/json" },
    })
      .then(function (r) {
        return r.json();
      })
      .then(applyAvailability)
      .catch(function () {
        showHint("Nie udało się sprawdzić dostępności. Odśwież stronę.", true);
      });
  }

  function scheduleFetch() {
    clearTimeout(fetchTimer);
    fetchTimer = setTimeout(fetchAvailability, 200);
  }

  function applyAvailability(data) {
    var rt = roomSelector.value;
    blockedCheckin = rt
      ? data.blocked_checkin || []
      : data.blocked_checkin_all || data.blocked_checkin || [];
    blockedCheckout = data.blocked_checkout || [];
    var types = data.room_types || [];
    var hasDates = checkInInput.value && checkOutInput.value;

    for (var i = 0; i < roomSelector.options.length; i++) {
      var opt = roomSelector.options[i];
      if (!opt.value) continue;
      var info = types.find(function (t) {
        return t.room_type === opt.value;
      });
      if (!info) continue;
      var full = hasDates && !info.available;
      opt.disabled = full;
      opt.hidden = full;
      var base = opt.getAttribute("data-name") || opt.value;
      if (hasDates) {
        opt.textContent =
          base +
          (full
            ? " — brak miejsc (" + info.label + ")"
            : " — wolne: " + info.free + "/" + info.capacity);
      }
    }

    if (roomSelector.value) {
      var sel = types.find(function (t) {
        return t.room_type === roomSelector.value;
      });
      if (hasDates && sel && !sel.available) {
        roomSelector.value = "";
        showHint("Wybrany typ jest niedostępny w tym terminie. Wybierz inny pokój lub daty.", true);
      } else if (hasDates && sel) {
        showHint("Obłożenie: " + sel.label + " (szczyt w wybranym terminie).", false);
      }
    }

    if (hasDates) {
      var anyFree = types.some(function (t) {
        return t.available;
      });
      if (!anyFree) {
        showHint("Wszystkie kategorie są zajęte w wybranym terminie.", true);
      }
    } else if (checkInInput.value || checkOutInput.value) {
      showHint("Wybierz datę przyjazdu i wyjazdu, aby zobaczyć dostępność.", false);
    } else {
      showHint("", false);
    }

    document.dispatchEvent(new CustomEvent("aladu:availability-updated"));
  }

  function validateDateInput(input, blocked, message) {
    if (!input.value) return true;
    if (blocked.indexOf(input.value) !== -1) {
      input.setCustomValidity(message);
      input.reportValidity();
      input.value = "";
      showHint(message, true);
      return false;
    }
    input.setCustomValidity("");
    return true;
  }

  checkInInput.addEventListener("change", function () {
    checkOutInput.min = checkInInput.value || checkInInput.min;
    if (!validateDateInput(checkInInput, blockedCheckin, "Ta data przyjazdu jest już w pełni zajęta dla wybranego typu pokoju.")) {
      scheduleFetch();
      return;
    }
    scheduleFetch();
  });

  checkOutInput.addEventListener("change", function () {
    if (
      !validateDateInput(
        checkOutInput,
        blockedCheckout,
        "Ten termin wyjazdu nie jest możliwy — brak wolnych pokoi w którejś z nocy pobytu."
      )
    ) {
      scheduleFetch();
      return;
    }
    scheduleFetch();
  });

  roomSelector.addEventListener("change", scheduleFetch);

  scheduleFetch();
})();
