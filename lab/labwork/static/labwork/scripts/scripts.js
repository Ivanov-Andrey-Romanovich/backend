function removeClass(obj, cls) {
    var classes = obj.className.split(' ');
    for (var i = 0; i < classes.length; i++) {
      if (classes[i] == cls) {
        classes.splice(i, 1);
        i--;
      }
    }
    obj.className = classes.join(' ');
  };
  function addClass(obj, cls) {
    var classes = obj.className ? obj.className.split(' ') : [];
    for (var i = 0; i < classes.length; i++) {
      if (classes[i] == cls) return; 
    }
    classes.push(cls); 
    obj.className = classes.join(' '); 
  } 
  window.activateTab = function(name){
  var tabs = document.getElementsByClassName('tabs__header__tab');
  var items = document.getElementsByClassName('tabs__body__item');
  for (var i=0; i < tabs.length; i++){
    var tab = tabs[i];
    removeClass(tab, "active"); 
    }
  for (var k=0; k < items.length; k++){
    var item = items[k];
    removeClass(item, "active"); 
    };
      var names = document.getElementsByName(name);
    addClass(names[0], "active");
    for(var z=0; z<tabs.length; z++){
   if (tabs[z].className === 'tabs__header__tab active'){
   addClass(items[z], "active") 
    }; 
    };
  };