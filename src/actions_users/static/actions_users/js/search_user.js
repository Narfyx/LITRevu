new Autocomplete('#autocomplete', {
    search: input => {
      console.log(input);
      const url = `/search_user/?user=${input}`;
      return new Promise(resolve => {
        fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
          resolve(data.data);
        });
      });
    },
    getResultValue: result => result,
    onSubmit: result => {
      // Here you handle the form submission
      // Prevent the default form submission
      event.preventDefault();
      const username = document.querySelector('.autocomplete-input').value;
      // Change form action based on the username
      const form = document.getElementById('userForm');
      form.action = `/follow/${username}/`;
    }
  });
  