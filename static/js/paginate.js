$(function () {
  var pg_links = $(".pg-link"),
    h_elm = $("#m-pg-link"),
    curr = 5,
    _this,
    _class,
    _id,
    __this,
    _num,
    i = 0;

  function changeNumbers(flag) {
    if ((curr > 2 && flag == 0) || flag) {
      if (curr == 1) {
        curr = 2;
        h_elm.removeClass("left");
        return;
      }

      $(pg_links).each(function () {
        __this = $(this).find("span");
        _num = parseInt(__this.text());

        if (flag) _num += 1;
        else _num -= 1;

        ++i;

        pg_links.addClass("s-hide");

        __this.text(_num);

        setTimeout(function () {
          pg_links.removeClass("s-hide");
        }, 150);

        if (i == 2) curr = _num;
      });

      i = 0;
    } else {
      if (curr == 2 && flag == 0) {
        curr = 1;
        h_elm.addClass("left");
      }
    }
  }

  function changeLinks() {
    _this = $(this);
    _class = _this.attr("class").trim().toLowerCase();

    if (_class == "arrow") {
      _id = _this.attr("id").trim().toLowerCase();

      if (_id == "l-arrow") changeNumbers(0);
      else changeNumbers(1);
    } else {
      if (parseInt(_this.text().trim()) < curr) changeNumbers(0);
      else changeNumbers(1);
    }
  }

  $(".pg-link,.arrow").on("click", changeLinks);
});