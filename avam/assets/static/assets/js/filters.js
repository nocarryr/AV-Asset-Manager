$(function(){
  var $filterDivs = $(".asset-list-filter"),
      $categoryUl = $(".asset-category-filter"),
      $manufUl = $(".asset-manufacturer-filter"),
      $templateLi = $("li", $categoryUl).clone(),
      $assetEl = $(".asset-list"),
      upgradeClasses = function(){
        $("[data-template-class]:not(.classes-upgraded)", $filterDivs).each(function(){
          var $el = $(this);
          $el.addClass($el.data('template-class')).addClass('classes-upgraded');
        });
        componentHandler.upgradeDom();
      },
      getCategories = function(){
        var objKeys = [],
            url = $categoryUl.data('href');
        $(".asset-list-item:visible", $assetEl).each(function(){
          objKeys.push({
            'name':'content_object',
            'value':$(this).data('contentObjectKey'),
          });
        });
        url = [url, $.param(objKeys)].join('?');
        $.get(url, function(data){
          var $data = $(data),
              $tempDiv = $('<div></div>');
          $tempDiv.hide().append($data).appendTo($("body"));
          $(".category-list li", $tempDiv).each(function(){
            var $dataLi = $(this),
                $newLi = $templateLi.clone(),
                itemId = 'asset-categories-' + $dataLi.data('categoryId').toString();
            $(".list-item-title", $newLi).text($dataLi.text());
            $("label", $newLi).attr('for', itemId);
            $(".input", $newLi).attr('id', itemId);
            $newLi
              .data('categoryId', $dataLi.data('categoryId'))
              .insertBefore($("li:last", $categoryUl));
            upgradeClasses();
            $tempDiv.remove();
          });
        });
      };
  $(".list-item-checkbox", $templateLi).prop('checked', false);
  upgradeClasses();
  getCategories();
  $("input", $manufUl).change(function(){
    var $this = $(this);
    console.log($this.prop('checked'));
  });
});
