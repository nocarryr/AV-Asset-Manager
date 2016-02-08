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
  $(".list-item-checkbox", $templateLi)
    .prop('checked', false)
    .removeClass('list-filter-all');
  upgradeClasses();
  getCategories();

  var filterHandler = function($listEl, filterParamCallback){
    $listEl.data('currentFilters', []);
    function refreshFilter(){
      var currentFilters = $listEl.data('currentFilters'),
          $filterEl = $("input:not(.list-filter-all)", $listEl),
          $allEl = $(".list-filter-all", $listEl);
      if (currentFilters.length == 0){
        $filterEl.prop('checked', false);
        $allEl.prop('checked', true);
      } else {
        $allEl.prop('checked', false);
      }
      $("input", $listEl).trigger('checkToggleState');
      $listEl.trigger('refreshFilter');
    }
    $("input", $listEl).change(function(){
      var $this = $(this),
          checked = $this.prop('checked'),
          objId = filterParamCallback($this),
          currentFilters = $listEl.data('currentFilters'),
          i = currentFilters.indexOf(objId);
      if ($this.hasClass('list-filter-all')){
        objId == 'ALL';
      }
      if (objId == 'ALL'){
        if (checked){
          currentFilters.splice(0, currentFilters.length);
        }
      } else {
        if (checked){
          if (i == -1){
            currentFilters.push(objId);
          }
        } else {
          if (i != -1){
            currentFilters.splice(i, 1);
          }
        }
      }
      refreshFilter();
    }).on('checkToggleState', function(){
      $(this).parent()[0].MaterialCheckbox.checkToggleState();
    });
  };

  filterHandler($manufUl, function($el){
    return $el.parents("li").data('objectId');
  });

  $manufUl.on('refreshFilter', function(){
    $(".asset-list-item").trigger('filterManufacturer');
  });

  $(".asset-list-item").on('filterManufacturer', function(){
    var $this = $(this),
        currentFilters = $manufUl.data('currentFilters'),
        i = currentFilters.indexOf($this.data('manufacturerId'));
    if (i != -1 || currentFilters.length == 0){
      $this.show();
    } else {
      $this.hide();
    }
  });
});
