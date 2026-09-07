// ==========================================================================
// ElectroMart - Main Frontend JavaScript
// Handles: theme toggle, toasts, wishlist/cart AJAX, mobile menu, live search
// ==========================================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ========== THEME SWITCHER (Dark / Light Mode) ==========
    var themeToggleBtn = document.getElementById('theme-toggle');
    
    if (themeToggleBtn) {
        // Get saved theme or default to light
        var currentTheme = localStorage.getItem('theme');
        if (!currentTheme) {
            currentTheme = 'light';
        }
        updateThemeUI(currentTheme);

        // When user clicks theme button
        themeToggleBtn.addEventListener('click', function() {
            // Get current theme
            var activeTheme = document.documentElement.getAttribute('data-theme');
            if (!activeTheme) {
                activeTheme = 'light';
            }
            
            // Switch theme
            var newTheme = 'light';
            if (activeTheme === 'light') {
                newTheme = 'dark';
            }
            
            // Apply new theme
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeUI(newTheme);
            showToast('Switched to ' + newTheme.toUpperCase() + ' mode', 'info');
        });
    }

    // Function to update theme button icon and text
    function updateThemeUI(theme) {
        if (!themeToggleBtn) return;
        
        var icon = themeToggleBtn.querySelector('i');
        var text = themeToggleBtn.querySelector('.theme-text');
        
        if (theme === 'dark') {
            if (icon) {
                icon.className = 'fas fa-sun';
            }
            if (text) {
                text.textContent = 'Light';
            }
        } else {
            if (icon) {
                icon.className = 'fas fa-moon';
            }
            if (text) {
                text.textContent = 'Dark';
            }
        }
    }

    // ========== AUTO DISMISS TOASTS ==========
    var toasts = document.querySelectorAll('.toast');
    for (var i = 0; i < toasts.length; i++) {
        var toast = toasts[i];
        setTimeout(function(toastElement) {
            return function() {
                toastElement.style.opacity = '0';
                toastElement.style.transform = 'translateX(100%)';
                setTimeout(function() {
                    toastElement.remove();
                }, 300);
            };
        }(toast), 4000);
    }

    // ========== WISHLIST AJAX TOGGLE ==========
    var wishlistBtns = document.querySelectorAll('.ajax-wishlist');
    
    for (var i = 0; i < wishlistBtns.length; i++) {
        var btn = wishlistBtns[i];
        
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            var url = this.dataset.url;
            if (!url) {
                url = this.getAttribute('href');
            }
            
            // Send AJAX request
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(function(response) {
                // Check if user is not logged in (401)
                if (response.status === 401) {
                    return response.json().then(function(data) {
                        var message = data.message;
                        if (!message) {
                            message = 'Please log in to save products for later.';
                        }
                        showToast(message, 'warning');
                        setTimeout(function() {
                            var redirectUrl = data.redirect_url;
                            if (!redirectUrl) {
                                redirectUrl = '/login/';
                            }
                            window.location.href = redirectUrl;
                        }, 1200);
                    });
                }
                
                // If response is ok
                if (response.ok) {
                    return response.json().then(function(data) {
                        if (data.success) {
                            var icon = this.querySelector('i');
                            
                            if (data.action === 'added') {
                                this.classList.add('active');
                                if (icon) {
                                    icon.className = 'fas fa-heart';
                                }
                                var msg = data.message;
                                if (!msg) {
                                    msg = 'Saved to your Wishlist';
                                }
                                showToast(msg, 'success');
                            } else {
                                this.classList.remove('active');
                                if (icon) {
                                    icon.className = 'far fa-heart';
                                }
                                var msg = data.message;
                                if (!msg) {
                                    msg = 'Removed from your Wishlist';
                                }
                                showToast(msg, 'info');
                            }
                        }
                    }.bind(this));
                } else {
                    // Fallback: redirect normally
                    window.location.href = url;
                }
            }.bind(this))
            .catch(function(err) {
                console.error('Wishlist error:', err);
                window.location.href = url;
            });
        });
    }

    // ========== AJAX ADD TO CART ==========
    var addCartBtns = document.querySelectorAll('.ajax-add-cart');

    for (var i = 0; i < addCartBtns.length; i++) {
        var btn = addCartBtns[i];

        btn.addEventListener('click', function(e) {
            e.preventDefault();

            var clickedBtn = this;
            if (clickedBtn.disabled) { return; }

            var url = clickedBtn.dataset.url;
            var csrfToken = getCookie('csrftoken');
            var originalIcon = clickedBtn.innerHTML;

            // Instant visual feedback so the click always feels real -
            // no waiting on the network to know something happened.
            clickedBtn.disabled = true;
            clickedBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(function(response) {
                // If not logged in (401)
                if (response.status === 401) {
                    return response.json().then(function(data) {
                        var message = data.message;
                        if (!message) {
                            message = 'Please log in to add products to cart.';
                        }
                        clickedBtn.innerHTML = originalIcon;
                        clickedBtn.disabled = false;
                        showToast(message, 'warning');
                        setTimeout(function() {
                            var redirectUrl = data.redirect_url;
                            if (!redirectUrl) {
                                redirectUrl = '/login/';
                            }
                            window.location.href = redirectUrl;
                        }, 1200);
                    });
                }

                if (response.ok) {
                    return response.json().then(function(data) {
                        if (data.success) {
                            var badges = document.querySelectorAll('.cart-badge');
                            for (var b = 0; b < badges.length; b++) {
                                badges[b].textContent = data.cart_total;
                            }
                            // Success checkmark flash right on the button that was clicked.
                            clickedBtn.innerHTML = '<i class="fas fa-check"></i>';
                            clickedBtn.style.background = 'var(--accent-emerald, #10b981)';
                            showToast('Item added to cart!', 'success');
                            setTimeout(function() {
                                clickedBtn.innerHTML = originalIcon;
                                clickedBtn.style.background = '';
                                clickedBtn.disabled = false;
                            }, 1400);
                        } else {
                            clickedBtn.innerHTML = originalIcon;
                            clickedBtn.disabled = false;
                            if (data.message) { showToast(data.message, 'error'); }
                        }
                    });
                } else {
                    return response.json().then(function(data) {
                        var message = data.message;
                        if (!message) {
                            message = 'Error adding product to cart.';
                        }
                        clickedBtn.innerHTML = originalIcon;
                        clickedBtn.disabled = false;
                        showToast(message, 'error');
                    });
                }
            })
            .catch(function(err) {
                console.error('Cart add error:', err);
                clickedBtn.innerHTML = originalIcon;
                clickedBtn.disabled = false;
                showToast('Network error. Please try again.', 'error');
            });
        });
    }

    // ========== PRODUCT DETAIL: ADD TO CART (validated, no page reload) ==========
    var addToCartForm = document.getElementById('addToCartForm');
    if (addToCartForm) {
        addToCartForm.addEventListener('submit', function(e) {
            e.preventDefault();

            var qtyInput = document.getElementById('id_quantity');
            var errorBox = document.getElementById('quantityError');
            var errorText = errorBox ? errorBox.querySelector('span') : null;
            var stock = parseInt(addToCartForm.dataset.stock, 10) || 0;
            var qty = parseInt(qtyInput.value, 10);

            // ---- Client-side validation ----
            var errorMsg = '';
            if (!qty || isNaN(qty) || qty < 1) {
                errorMsg = 'Please enter a valid quantity (at least 1).';
            } else if (qty > stock) {
                errorMsg = 'Only ' + stock + ' unit(s) available in stock.';
            }

            if (errorMsg) {
                qtyInput.classList.add('input-invalid');
                qtyInput.style.borderColor = '#e11d48';
                if (errorBox && errorText) {
                    errorText.textContent = errorMsg;
                    errorBox.style.display = 'block';
                }
                return;
            }

            qtyInput.classList.remove('input-invalid');
            qtyInput.style.borderColor = '';
            if (errorBox) { errorBox.style.display = 'none'; }

            var submitBtn = addToCartForm.querySelector('button[type="submit"]');
            var originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            }

            var csrfToken = getCookie('csrftoken');
            var formData = new FormData(addToCartForm);

            fetch(addToCartForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(function(response) {
                if (response.status === 401) {
                    return response.json().then(function(data) {
                        window.location.href = data.redirect_url || '/login/';
                    });
                }
                return response.json().then(function(data) {
                    if (data.success) {
                        var badges = document.querySelectorAll('.cart-badge');
                        for (var i = 0; i < badges.length; i++) {
                            badges[i].textContent = data.cart_total;
                        }
                        // Instant redirect to the cart page - no waiting, no delay.
                        window.location.href = addToCartForm.dataset.cartUrl || '/cart/';
                    } else {
                        showToast(data.message || 'Error adding product to cart.', 'error');
                        if (submitBtn) {
                            submitBtn.disabled = false;
                            submitBtn.innerHTML = originalBtnHtml;
                        }
                    }
                });
            })
            .catch(function(err) {
                console.error('Add to cart error:', err);
                showToast('Something went wrong. Please try again.', 'error');
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnHtml;
                }
            });
        });

        // Clear the error as soon as the user fixes the quantity.
        var qtyInputEl = document.getElementById('id_quantity');
        if (qtyInputEl) {
            qtyInputEl.addEventListener('input', function() {
                var errorBox = document.getElementById('quantityError');
                qtyInputEl.style.borderColor = '';
                if (errorBox) { errorBox.style.display = 'none'; }
            });
        }
    }

    // ========== GENERIC REAL-TIME FORM VALIDATION ==========
    // Applies to login / register / checkout forms. Adds instant visual
    // feedback (red border + inline message) for required fields, email
    // format, and minimum lengths -- without blocking Django's own
    // server-side validation, which always runs too.
    var validatedForms = document.querySelectorAll('.auth-container form, #checkoutForm');

    function fieldError(el, msg) {
        el.classList.add('input-invalid');
        el.style.borderColor = '#e11d48';
        var next = el.nextElementSibling;
        if (!next || !next.classList || !next.classList.contains('field-live-error')) {
            var span = document.createElement('div');
            span.className = 'field-live-error';
            span.style.cssText = 'color:#e11d48;font-size:0.8rem;margin-top:0.3rem;font-weight:600;';
            el.insertAdjacentElement('afterend', span);
            next = span;
        }
        next.innerHTML = '<i class="fas fa-circle-exclamation"></i> ' + msg;
        next.style.display = 'block';
    }

    function fieldClear(el) {
        el.classList.remove('input-invalid');
        el.style.borderColor = '';
        var next = el.nextElementSibling;
        if (next && next.classList && next.classList.contains('field-live-error')) {
            next.style.display = 'none';
        }
    }

    function validateField(el) {
        var value = el.value.trim();

        if (el.hasAttribute('required') && !value) {
            fieldError(el, 'This field is required.');
            return false;
        }
        if (el.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
            fieldError(el, 'Enter a valid email address.');
            return false;
        }
        if (el.type === 'password' && value && value.length < 8) {
            fieldError(el, 'Password must be at least 8 characters.');
            return false;
        }
        if (el.name === 'phone_number' && value) {
            var digits = value.replace(/\D/g, '');
            if (digits.length < 7) {
                fieldError(el, 'Enter a valid phone number (at least 7 digits).');
                return false;
            }
        }
        if (el.hasAttribute('minlength') && value && value.length < parseInt(el.getAttribute('minlength'), 10)) {
            fieldError(el, 'Must be at least ' + el.getAttribute('minlength') + ' characters.');
            return false;
        }

        fieldClear(el);
        return true;
    }

    for (var vf = 0; vf < validatedForms.length; vf++) {
        var vform = validatedForms[vf];
        var inputs = vform.querySelectorAll('input, select, textarea');

        for (var vi = 0; vi < inputs.length; vi++) {
            (function(input) {
                input.addEventListener('blur', function() { validateField(input); });
                input.addEventListener('input', function() {
                    if (input.classList.contains('input-invalid')) {
                        validateField(input);
                    }
                });
            })(inputs[vi]);
        }

        vform.addEventListener('submit', function(e) {
            var formInputs = this.querySelectorAll('input, select, textarea');
            var isValid = true;
            for (var k = 0; k < formInputs.length; k++) {
                if (!validateField(formInputs[k])) {
                    isValid = false;
                }
            }
            if (!isValid) {
                e.preventDefault();
                var firstInvalid = this.querySelector('.input-invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                showToast('Please fix the highlighted fields.', 'error');
            }
        });
    }

    // ========== CSRF TOKEN HELPER ==========
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ========== SMOOTH CART UPDATES (no full page reload) ==========
    // Handles quantity-update and remove/save-for-later forms inside #cartAjaxRoot.
    // Uses event delegation so it keeps working after the DOM is swapped below.
    document.addEventListener('submit', function(e) {
        var form = e.target;
        if (!form.classList || !form.classList.contains('cart-ajax-form')) {
            return;
        }
        e.preventDefault();

        var submitter = e.submitter; // the button that triggered submit (e.g. "Save for Later")
        var formData = new FormData(form);
        if (submitter && submitter.name) {
            formData.append(submitter.name, submitter.value);
        }

        var root = document.getElementById('cartAjaxRoot');
        if (root) {
            root.style.opacity = '0.55';
            root.style.pointerEvents = 'none';
        }

        fetch(form.action, {
            method: form.method || 'POST',
            body: formData
        })
        .then(function(response) { return response.text(); })
        .then(function(html) {
            var parser = new DOMParser();
            var doc = parser.parseFromString(html, 'text/html');

            // Swap the cart section in place -- no navigation, no flash of a blank page.
            var newRoot = doc.getElementById('cartAjaxRoot');
            if (newRoot && root) {
                root.innerHTML = newRoot.innerHTML;
                root.style.opacity = '';
                root.style.pointerEvents = '';
            } else {
                // Fallback: if the server redirected somewhere unexpected, just reload.
                window.location.reload();
                return;
            }

            // Sync every cart badge on the page (desktop + mobile nav).
            var newBadges = doc.querySelectorAll('.cart-badge');
            var badges = document.querySelectorAll('.cart-badge');
            if (newBadges.length && badges.length) {
                var newVal = newBadges[0].textContent;
                for (var i = 0; i < badges.length; i++) {
                    badges[i].textContent = newVal;
                }
            }

            // Surface any Django message (e.g. "removed from cart") as a toast.
            var newMsg = doc.querySelector('.messages-container .toast, .alert');
            if (newMsg) {
                showToast(newMsg.textContent.trim(), 'success');
            }
        })
        .catch(function(err) {
            console.error('Cart update error:', err);
            if (root) {
                root.style.opacity = '';
                root.style.pointerEvents = '';
            }
            window.location.reload();
        });
    });

    // ========== DYNAMIC TOAST CREATOR ==========
    function showToast(message, type) {
        if (!type) {
            type = 'success';
        }
        
        // Find or create messages container
        var container = document.querySelector('.messages-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'messages-container';
            document.body.appendChild(container);
        }
        
        // Create toast element
        var toast = document.createElement('div');
        toast.className = 'toast toast-' + type;

        // Icon based on type
        var iconMap = { success: 'fa-check-circle', error: 'fa-exclamation-circle', warning: 'fa-exclamation-triangle', info: 'fa-info-circle' };
        var icon = iconMap[type] || 'fa-info-circle';
        toast.innerHTML = '<i class="fas ' + icon + '"></i> ' + message;
        
        // Add to container
        container.appendChild(toast);
        
        // Auto remove after 3.5 seconds
        setTimeout(function() {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(function() {
                if (toast.parentNode) toast.remove();
            }, 300);
        }, 3500);
    }

    // Expose globally so mobile burger menu code (outside DOMContentLoaded) can use them
    window.showToast = showToast;
    window._updateThemeUI = updateThemeUI;

}); // end DOMContentLoaded


// ========== BACK TO TOP BUTTON ==========
var backToTopBtn = document.getElementById('backToTopBtn');

if (backToTopBtn) {
    // Show button when user scrolls down 300px from top
    window.addEventListener('scroll', function() {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            backToTopBtn.style.display = 'flex';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });

    // Scroll to top smoothly when clicked
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ========== BURGER MENU (Mobile Responsive) ==========
var burgerBtn = document.getElementById('burgerMenuBtn');
var mobileMenu = document.getElementById('mobileMenu');
var mobileThemeToggle = document.getElementById('mobileThemeToggle');

if (burgerBtn && mobileMenu) {
    // Show burger icon only on mobile
    function checkScreenSize() {
        if (window.innerWidth <= 640) {
            burgerBtn.style.display = 'block';
        } else {
            burgerBtn.style.display = 'none';
            mobileMenu.style.display = 'none';
        }
    }
    
    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);

    // Toggle menu on click
    burgerBtn.addEventListener('click', function() {
        if (mobileMenu.style.display === 'none') {
            mobileMenu.style.display = 'block';
            burgerBtn.querySelector('i').className = 'fas fa-times';
        } else {
            mobileMenu.style.display = 'none';
            burgerBtn.querySelector('i').className = 'fas fa-bars';
        }
    });
}

// ========== MOBILE THEME TOGGLE ==========
if (mobileThemeToggle) {
    mobileThemeToggle.addEventListener('click', function() {
        var activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
        var newTheme = activeTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        if (window._updateThemeUI) window._updateThemeUI(newTheme);
        if (window.showToast) window.showToast('Switched to ' + newTheme.toUpperCase() + ' mode', 'info');
    });
}


// ========== SEARCH SUGGESTIONS (Autocomplete) ==========
var searchInput = document.getElementById('searchInput');
var suggestionsBox = document.getElementById('searchSuggestions');

if (searchInput) {
    // Input event – show suggestions while typing
    searchInput.addEventListener('input', function() {
        var query = this.value.trim();
        
        if (query.length >= 2) {
            fetch('/search-suggestions/?q=' + encodeURIComponent(query))
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = '';
                    if (data.products.length > 0) {
                        data.products.forEach(function(product) {
                            var item = document.createElement('a');
                            item.href = '/product/' + product.slug + '/';
                            item.style.display = 'flex';
                            item.style.alignItems = 'center';
                            item.style.gap = '0.75rem';
                            item.style.padding = '0.5rem 0.75rem';
                            item.style.textDecoration = 'none';
                            item.style.color = 'var(--text-main)';
                            item.style.borderBottom = '1px solid var(--border-color)';
                            
                            item.innerHTML = `
                                <img src="${product.image}" alt="${product.name}" style="width: 40px; height: 40px; object-fit: cover; border-radius: var(--radius-sm);">
                                <div>
                                    <div style="font-weight: 600; font-size: 0.9rem;">${product.name}</div>
                                    <div style="font-size: 0.8rem; color: var(--primary); font-weight: 700;">$${product.price}</div>
                                </div>
                            `;
                            suggestionsBox.appendChild(item);
                        });
                        suggestionsBox.style.display = 'block';
                    } else {
                        suggestionsBox.style.display = 'none';
                    }
                });
        } else {
            suggestionsBox.style.display = 'none';
        }
    });

    // Keydown event – submit form on Enter key
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            var query = this.value.trim();
            if (query.length >= 1) {
                this.form.submit();  // Form submit karo
            }
        }
    });

    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = 'none';
        }
    });
}