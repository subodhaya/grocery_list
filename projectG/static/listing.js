document.addEventListener('DOMContentLoaded', function() {


    document.getElementById("created_list").addEventListener("click", function() {
      var createdView = document.getElementById("created-view");
      createdView.style.display = "none"; 
      var listsContainer = document.getElementById("lists-container");
      listsContainer.style.display = "none";
      }); 

    
    
    

        // Make an AJAX request to the Django view to get list names

    //document.querySelector('#compose-form').addEventListener('submit', send_email);
    //document.querySelector('#saved_list').addEventListener('click', () => load_lists('saved_list'));
    
    
      //document.querySelector('#finished_task').addEventListener('click', () => load_lists('finished_task'));
    }); 
    
    let currentList = null;
        const lists = {};

    
    function toggleListItems(listElement) {
        var listItems = listElement.querySelector('.list-items');
        
        if (listItems.style.display === "none") {
            listItems.style.display = "block";
        } else {
            listItems.style.display = "none";
        }
    }
    
    const listNames = document.querySelectorAll('.list h3');
    listNames.forEach(listName => {
        listName.addEventListener('click', function () {
            const listItems = listName.nextElementSibling;
            if (listItems.style.display === 'none' || listItems.style.display === '') {
                listItems.style.display = 'block';
            } else {
                listItems.style.display = 'none';
            }
        });
    }); 
    
    
    
    function createList() {
    
        const listNameInput = document.getElementById('listName');
        const listName = listNameInput.value.trim();
    
        if (listName !== '') {
          currentList = listName;
          document.getElementById('currentListName').textContent = `List: ${currentList}`;
          document.getElementById('groceryListContainer').style.display = 'none';
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
    
            newItem.addEventListener('click', function() {
              toggleDone(newItem);
            });
    
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
    