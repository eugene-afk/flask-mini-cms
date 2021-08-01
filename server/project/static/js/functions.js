document.addEventListener('DOMContentLoaded', () => {
    eva.replace({
        type: "flip",
        hover: true,
        infinite: false,
    });
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
      const $notification = $delete.parentNode;
  
      $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
      });
    });

    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if($navbarBurgers.length > 0){
      $navbarBurgers.forEach(el => {
        el.addEventListener('click', ()=>{
          const target = el.dataset.target;
          const $target = document.getElementById(target);

          el.classList.toggle('is-active');
          $target.classList.toggle('is-active')
        })
      });
    }

  });