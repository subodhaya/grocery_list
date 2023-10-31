document.addEventListener('DOMContentLoaded', function() {


  document.getElementById("created_list").addEventListener("click", function() {
    var createdView = document.getElementById("created-view");
    createdView.style.display = "block"; 
    var listsContainer = document.getElementById("lists-container");
        listsContainer.style.display = "none";
    }); 
  
  // Use buttons to toggle between views
  document.getElementById("allList").addEventListener("click", function() {
      window.location.href = "/projectG/";
      var listsContainer = document.getElementById("lists-container");
      var lists = listsContainer.querySelectorAll(".list");
  
      lists.forEach(function(list) {
          if (list.style.display === "none") {
              list.style.display = "block";
          } else {
              list.style.display = "none";
          }
      }); 
  });
  document.getElementById("get_finished_lists").addEventListener("click", function() {
     
        
      fetch(`/projectG/get_finished_lists/`)  // Replace with the actual URL of your view
        
        .then(response => {
          if (response.ok) {
            // If the response status is OK, redirect to the response URL
            window.location.href = response.url;
          } else {
            console.error("Error fetching finished lists. Status:", response.status);
          }
        })
        .catch(error => {
          console.error("Error fetching finished lists:", error);
        });
    });
      
    //document.querySelector('#finished_task').addEventListener('click', () => load_lists('finished_task'));
  }); 
  
  document.getElementById("saved_list").addEventListener("click", function() {
     
        
     fetch(`/projectG/get_saved_lists/`)  // Replace with the actual URL of your view
       
       .then(response => {
         if (response.ok) {
           // If the response status is OK, redirect to the response URL
           window.location.href = response.url;
         } else {
           console.error("Error fetching finished lists. Status:", response.status);
         }
       })
       .catch(error => {
         console.error("Error fetching finished lists:", error);
       });
   });
     
   //document.querySelector('#finished_task').addEventListener('click', () => load_lists('finished_task'));
  
  
  
  
  let currentList = null;
      const lists = {};
  
      function shopNow(listId) {
      // Fetch the list data for the specified listId using AJAX
      fetch(`/projectG/get_items/${listId}/`)
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.json();
          })
          .then(data => {
              // Extract the list name and items from the response
              const listName = data.list_name; // Adjust this based on the actual structure of your JSON response
              const items = data.items; // Adjust this based on the actual structure of your JSON response
              const url = `{% url 'shopnow_view' list_id=0 %}`.replace('0', listId);
  
     
              // Encode the data as a query string
              const queryString = `?list_name=${encodeURIComponent(listName)}&items=${encodeURIComponent(JSON.stringify(items))}`;
              const finalUrl = `${url}${queryString}`;
              // Redirect to the shopnow.html page with the query string
              window.location.href = finalUrl;
          })
          
  }
  
  
  function toggleListItems(listElement) {
      var listItems = listElement.querySelector('.list-items');
      
      
      if (listItems.style.display === "none") {
          
          listItems.style.display = "block";
      } else {
          listItems.style.display = "none";
      }
  }
     
  
  
  function toggleListStatus(listId, button) {
      // Simulate toggling the "saved_list" status
      const saved_list = !button.dataset.saved_list || button.dataset.saved_list === 'false';
      button.dataset.saved_list = saved_list;
      
      // Update the button text based on the new status
      button.textContent = saved_list ? 'saved_list' : 'Not saved_list';
  
      // You can send an AJAX request to update the server-side status here
      // Example AJAX request to update the status on the server:
      
      fetch(`/projectG/update_list_status/${listId}/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
          },
          body: JSON.stringify({ saved_list }), // Send the new status
      })
      .then(response => {
          if (response.ok) {
              // Status updated successfully
          } else {
              // Error updating status
          }
      })
      .catch(error => {
          console.log('Error:', error);
      });
      
  }
  
  function toggleTaskStatus(listId, button) {
      // Simulate toggling the "finished" status
      const finished = !button.dataset.finished || button.dataset.finished === 'false';
      button.dataset.finished = finished;
      
      // Update the button text based on the new status
      button.textContent = finished ? 'Finished' : 'Not Finished';
  
      // You can send an AJAX request to update the server-side status here
      // Example AJAX request to update the status on the server:
      
      fetch(`/projectG/update_task_status/${listId}/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
          },
          body: JSON.stringify({ finished }), // Send the new status
      })
      .then(response => {
          if (response.ok) {
              // Status updated successfully
          } else {
              // Error updating status
          }
      })
      .catch(error => {
          console.log('Error:', error);
      });
      
  }
  
  // Function to get the CSRF token from the cookie (if needed)
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  
  
  
  function createList() {
  
      const listNameInput = document.getElementById('listName');
      const listName = listNameInput.value.trim();
  
      if (listName !== '') {
        currentList = listName;
        document.getElementById('currentListName').textContent = `List: ${currentList}`;
        document.getElementById('groceryListContainer').style.display = 'block';
        listNameInput.value = '';
      }
    }
  
    function toggleDone(item) {
      item.classList.toggle('done');
    }
  
    function addItem() {
      if (currentList) {
        
        const itemInput = document.getElementById('itemName');
        const itemQuantityInput = document.getElementById('itemQuantity');
        const itemInstructionInput = document.getElementById('itemInstruction');
        
        const itemName = itemInput.value.trim();
        const itemQuantity = itemQuantityInput.value.trim();
        const itemInstruction = itemInstructionInput.value.trim();
  
        if (itemName !== '') {
          const groceryItems = document.getElementById('groceryItems');
          const newItem = document.createElement('li');
          newItem.className = 'list-item';
          
          const itemNameSpan = document.createElement('span');
          itemNameSpan.textContent = itemName;
          
          const quantitySpan = document.createElement('span');
          quantitySpan.textContent = `Quantity: ${itemQuantity}`;
          
          const instructionSpan = document.createElement('span');
          instructionSpan.textContent = `Instruction: ${itemInstruction}`;
  
          const editButton = document.createElement('button');
          editButton.textContent = 'Edit';
          editButton.addEventListener('click', function() {
            const editedItemName = prompt('Enter or edit item name:', itemName);
            const editedQuantity = prompt('Enter or edit quantity:', itemQuantity);
            const editedInstruction = prompt('Enter or edit instruction:', itemInstruction);
  
            if (editedItemName !== null && editedQuantity !== null && editedInstruction !== null) {
              itemNameSpan.textContent = editedItemName;
              quantitySpan.textContent = `Quantity: ${editedQuantity}`;
              instructionSpan.textContent = `Instruction: ${editedInstruction}`;
            } 
          });
  
          const deleteButton = document.createElement('button');
          deleteButton.textContent = 'Delete';
          deleteButton.addEventListener('click', function() {
            groceryItems.removeChild(newItem);
          });
          
          const buttonContainer = document.createElement('div');
          buttonContainer.className = 'list-item-buttons';
     
          
          newItem.appendChild(itemNameSpan);
          
          newItem.appendChild(quantitySpan);
          newItem.appendChild(instructionSpan);
          newItem.appendChild(buttonContainer);
          
          buttonContainer.appendChild(editButton);
          buttonContainer.appendChild(deleteButton);
  
         
  
          groceryItems.appendChild(newItem);
          itemInput.value = '';
          itemQuantityInput.value = '';
          itemInstructionInput.value = '';
        }
      }
    }
    function submitList() {
      if (currentList && document.getElementById('groceryItems').children.length > 0) {
        lists[currentList] = [];
        const groceryItems = document.getElementById('groceryItems').children;
        for (const item of groceryItems) {
          const itemName = item.querySelector('span:first-child').textContent;
          const quantity = item.querySelector('span:nth-child(2)').textContent;
          const instruction = item.querySelector('span:nth-child(3)').textContent;
          lists[currentList].push({ itemName, quantity, instruction });
        }
        console.log(lists);
        
        const data = JSON.stringify(lists);
  
  // Get the CSRF token from the cookie
  const csrftoken = getCookie('csrftoken');
  
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/projectG/log_lists/', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  
  // Set the CSRF token in the request header
  xhr.setRequestHeader('X-CSRFToken', csrftoken);
  
  xhr.onreadystatechange = function () {
      if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
              console.log('Data sent successfully');
          } else {
              console.log('Error sending data');
          }
      }
  };
  xhr.send(data);
  
  alert('List submitted successfully!');
  } else {
  alert('Please add items to the list before submitting.');
  }
  }
  
  // Function to get the CSRF token from the cookie
  function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
      }
  }
  }
  return cookieValue;
  }
  
  