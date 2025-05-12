const STORAGE_KEY = 'productFormData';



function saveFormData() {
  const form = document.getElementById('product-form');
  const data = {};
  new FormData(form).forEach((value, key) => {
    if (form.elements[key].type !== 'file') {
      data[key] = value;
    }
  });
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
}

document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const newCatId = params.get('category_id');
  const newSubCatId = params.get('subcategory_id');

  // if came back from category or subcategory
  if (newCatId || newSubCatId) {
    // restore everthing
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      const data = JSON.parse(saved);
      Object.entries(data).forEach(([name, value]) => {
        const field = document.querySelector(`[name="${name}"]`);
        if (field && field.type !== 'file') {
          field.value = value;
        }
      });
    }

    if(newCatId){
        const catField = document.querySelector('[name="category"]');
        if(catField){
            catField.value = newCatId;
        }
    }

    if(newSubCatId){
        const subCatField = document.querySelector('[name="subcategory"]');
        if(subCatField){
            subCatField.value = newSubCatId;
        }
    }

    // 3) então limpa o armazenamento
    localStorage.removeItem(STORAGE_KEY);
    return;
  }

  // Caso NORMAL (back button ou só navegação), restaura sem limpar
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    const data = JSON.parse(saved);
    Object.entries(data).forEach(([name, value]) => {
      const field = document.querySelector(`[name="${name}"]`);
      if (field && field.type !== 'file') {
        field.value = value;
      }
    });
  }
});

        
        //update the link of subcategory based on category
        const categoriaSelect = document.getElementById("id_category");
        const subcatLink = document.getElementById("new-subcategory-link");

        function UpdateHref(){
            const selectedId = categoriaSelect.value;
            const baseHref = subcatLink.dataset.base;
            const next = subcatLink.dataset.next;

            if (selectedId){
                subcatLink.href = `${baseHref}?category_id=${selectedId}&next=${encodeURIComponent(next)}`;
            }else{
                subcatLink.href = `${baseHref}?next=${encodeURIComponent(next)}`;
            }
        }

        categoriaSelect.addEventListener("change", UpdateHref);
        UpdateHref();