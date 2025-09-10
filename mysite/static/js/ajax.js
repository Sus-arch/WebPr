function ajaxRequest(url, method, data, successCallback, errorCallback) {
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

    const csrftoken = getCookie('csrftoken');

    const requestOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        credentials: 'same-origin'
    };

    if (method === 'POST' && data) {
        requestOptions.body = JSON.stringify(data);
    }

    fetch(url, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (successCallback) successCallback(data);
        })
        .catch(error => {
            console.error('Error:', error);
            if (errorCallback) errorCallback(error);
        });
}

function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        let date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function addToCart(productId) {
    ajaxRequest(
        '/ajax/add-to-cart/',
        'POST',
        { product_id: productId },
        function(data) {
            if (data.status === 'success') {
                updateCartCount(data.cart_count);

                setCookie('cart', JSON.stringify(data.cart), 30);

                showNotification(data.message, 'success');

                if (document.getElementById('cart-content')) {
                    loadCartContent();
                }
            } else {
                showNotification('Ошибка: ' + data.message, 'error');
            }
        },
        function(error) {
            showNotification('Ошибка сети: ' + error.message, 'error');
        }
    );
}

function removeFromCart(productId) {
    ajaxRequest(
        '/ajax/remove-from-cart/',
        'POST',
        { product_id: productId },
        function(data) {
            if (data.status === 'success') {
                updateCartCount(data.cart_count);

                setCookie('cart', JSON.stringify(data.cart), 30);

                showNotification(data.message, 'success');

                if (document.getElementById('cart-content')) {
                    loadCartContent();
                }
            } else {
                showNotification('Ошибка: ' + data.message, 'error');
            }
        },
        function(error) {
            showNotification('Ошибка сети: ' + error.message, 'error');
        }
    );
}

function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        element.textContent = count;
        element.style.display = count > 0 ? 'inline' : 'none';
    });
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

function loadCartContent() {
    const cartContent = document.getElementById('cart-content');
    if (!cartContent) return;

    cartContent.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
        </div>
    `;

    const cart = getCookie('cart');
    let cartData = {};

    try {
        cartData = cart ? JSON.parse(cart) : {};
    } catch (e) {
        console.error('Error parsing cart data:', e);
        cartContent.innerHTML = '<p class="text-center text-danger">Ошибка загрузки корзины</p>';
        return;
    }

    if (Object.keys(cartData).length === 0) {
        cartContent.innerHTML = '<p class="text-center">Корзина пуста</p>';
        return;
    }

    ajaxRequest(
        '/ajax/get-products/',
        'GET',
        null,
        function(data) {
            try {
                const products = Array.isArray(data.products)
                    ? data.products
                    : JSON.parse(data.products);

                cartContent.innerHTML = '';
                let total = 0;

                Object.keys(cartData).forEach(productId => {
                    const product = products.find(p => String(p.pk) === String(productId));
                    if (product) {
                        const fields = product.fields;
                        const quantity = cartData[productId];
                        const itemTotal = fields.price * quantity;
                        total += itemTotal;

                        const cartItem = document.createElement('div');
                        cartItem.className = 'cart-item d-flex justify-content-between align-items-center mb-3 p-3 border-bottom';
                        cartItem.innerHTML = `
                            <div class="flex-grow-1">
                                <h6 class="mb-1">${fields.name}</h6>
                                <small class="text-muted">${fields.price} руб. × ${quantity} шт.</small>
                            </div>
                            <div class="d-flex align-items-center">
                                <span class="me-3 fw-bold">${itemTotal} руб.</span>
                                <button class="btn btn-sm btn-danger remove-from-cart" data-product-id="${productId}">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </div>
                        `;

                        cartContent.appendChild(cartItem);
                    }
                });

                const totalElement = document.createElement('div');
                totalElement.className = 'd-flex justify-content-between align-items-center mt-4 pt-3 border-top';
                totalElement.innerHTML = `
                    <h5 class="mb-0">Итого:</h5>
                    <h5 class="mb-0">${total} руб.</h5>
                `;
                cartContent.appendChild(totalElement);

                document.querySelectorAll('.remove-from-cart').forEach(button => {
                    button.addEventListener('click', function() {
                        const productId = this.getAttribute('data-product-id');
                        removeFromCart(productId);
                    });
                });

            } catch (e) {
                console.error('Error processing products:', e);
                cartContent.innerHTML = '<p class="text-center text-danger">Ошибка загрузки корзины</p>';
            }
        },
        function(error) {
            console.error('Error loading products:', error);
            cartContent.innerHTML = '<p class="text-center text-danger">Ошибка загрузки корзины</p>';
        }
    );
}

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

document.addEventListener('DOMContentLoaded', function() {
    updateCartCounter();

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            addToCart(productId);
        });
    });

    if (document.getElementById('cart-content')) {
        loadCartContent();
    }
});

function updateCartCounter() {
    const cart = getCookie('cart');
    if (cart) {
        try {
            const cartData = JSON.parse(cart);
            const count = Object.values(cartData).reduce((a, b) => a + b, 0);
            updateCartCount(count);
        } catch (e) {
            console.error('Error parsing cart cookie:', e);
        }
    }
}