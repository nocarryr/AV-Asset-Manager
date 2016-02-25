$(function(){
  var $filterDivs = $(".asset-list-filter"),
      $categoryUl = $(".asset-category-filter"),
      $manufUl = $(".asset-manufacturer-filter"),
      $assetEl = $(".asset-list"),
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
              $tempDiv = $('<div></div>'),
              $itemList;
          $tempDiv.hide().append($data).appendTo($("body"));
          $itemList = $(".category-item-list", $tempDiv).detach();
          $(".category-data").empty().append($itemList);

          $(".category-list a", $tempDiv).each(function(){
            var $aTag = $(this),
                itemId = 'asset-categories-' + $aTag.data('categoryId').toString();
            $aTag
              .attr('id', itemId)
              .addClass('list-group-item')
              .insertBefore($("a:last", $categoryUl));
            $tempDiv.remove();
          });
        });
      };
  getCategories();

  var filterHandler = function($listEl, filterParamCallback){
    $listEl.data('currentFilters', []);
    function refreshFilter(){
      var currentFilters = $listEl.data('currentFilters'),
          $filterEl = $("a:not(.list-filter-all)", $listEl),
          $allEl = $(".list-filter-all", $listEl);
      if (currentFilters.length == 0){
        $filterEl.removeClass('active');
        $allEl.addClass('active');
      } else {
        $allEl.removeClass('active');
      }
      $listEl.trigger('refreshFilter');
    }
    $listEl.on('click', 'a', function(e){
      var $this = $(this);
      $this.toggleClass('active');
      var checked = $this.hasClass('active'),
          objId = filterParamCallback($this),
          currentFilters = $listEl.data('currentFilters'),
          i = currentFilters.indexOf(objId);
      if ($this.hasClass('list-filter-all')){
        objId = 'ALL';
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
    });
  };

  filterHandler($manufUl, function($el){
    return $el.data('objectId');
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

  filterHandler($categoryUl, function($el){
    return $el.attr('id');
  });

  $categoryUl.on('refreshFilter', function(){
    $(".asset-list-item").trigger('filterCategory');
  });

  $(".asset-list-item").on('filterCategory', function(){
    var $this = $(this),
        currentFilters = $categoryUl.data('currentFilters'),
        active = false;
    if (currentFilters.length == 0){
      active = true;
    } else {
      $.each(currentFilters, function(i, filtId){
        var $filt = $("#" + filtId),
            categoryId = $filt.data('categoryId'),
            sel = "[data-category-id=ID]".replace('ID', categoryId.toString()),
            cobjKey = $(sel, $(".category-item-list")).data('contentObjectKey');
        if ($this.data('contentObjectKey') == cobjKey){
          active = true;
          return false;
        }
      });
    }
    if (active){
      $this.show();
    } else {
      $this.hide();
    }
  });

  $(".asset-status-filter a").click(function(e){
    var $this = $(this),
        fieldName = $this.data('fieldname');
    e.preventDefault();
    $this.toggleClass('active');
    $(".asset-list-item").trigger('filterStatus', [fieldName, $this.hasClass('active')]);
  });
  $(".asset-list-item").on('filterStatus', function(e, fieldName, value){
    var $this = $(this),
        $td = $("[data-fieldname=F]".replace('F', fieldName), $this),
        fieldValue = $td.data('fieldvalue') == 'True';
    if (!fieldValue){
      return;
    }
    if (value){
      $this.show();
    } else {
      $this.hide();
    }
  });
});
