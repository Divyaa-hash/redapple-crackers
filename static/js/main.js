// Premium Fireworks - Main JavaScript

// ===== LOADING SCREEN =====
window.addEventListener('load', () => {
    const loadingScreen = document.getElementById('loading-screen');
    setTimeout(() => {
        loadingScreen.classList.add('hidden');
        setTimeout(() => {
            loadingScreen.style.display = 'none';
        }, 500);
    }, 1500);
});

// ===== SCROLL PROGRESS =====
window.addEventListener('scroll', () => {
    const scrollProgress = document.getElementById('scroll-progress');
    const scrollTop = document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const progress = (scrollTop / scrollHeight) * 100;
    scrollProgress.style.width = progress + '%';
});

// ===== GSAP ANIMATIONS =====
gsap.registerPlugin(ScrollTrigger);

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
if (navbar) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// Scroll reveal animations
const revealElements = document.querySelectorAll('.reveal');
revealElements.forEach(element => {
    gsap.fromTo(element, 
        { opacity: 0, y: 30 },
        {
            opacity: 1,
            y: 0,
            duration: 0.8,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: element,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        }
    );
});

// Stagger animations for cards
const cardGroups = document.querySelectorAll('.card-group');
cardGroups.forEach(group => {
    const cards = group.querySelectorAll('.product-card, .category-card');
    gsap.fromTo(cards,
        { opacity: 0, y: 50 },
        {
            opacity: 1,
            y: 0,
            duration: 0.6,
            stagger: 0.1,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: group,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        }
    );
});

// Parallax effect for hero
const heroSection = document.querySelector('.hero-section');
if (heroSection) {
    gsap.to(heroSection, {
        backgroundPosition: '50% 100%',
        ease: 'none',
        scrollTrigger: {
            trigger: heroSection,
            start: 'top top',
            end: 'bottom top',
            scrub: true
        }
    });
}

// ===== PARTICLES BACKGROUND =====
function createParticles() {
    const container = document.querySelector('.particles-container');
    if (!container) return;
    
    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 8 + 's';
        particle.style.animationDuration = (Math.random() * 4 + 6) + 's';
        container.appendChild(particle);
    }
}

createParticles();

// ===== MEGA MENU =====
const menuTriggers = document.querySelectorAll('.menu-trigger');
menuTriggers.forEach(trigger => {
    trigger.addEventListener('mouseenter', () => {
        const megaMenu = trigger.querySelector('.mega-menu');
        if (megaMenu) {
            megaMenu.classList.add('open');
        }
    });
    
    trigger.addEventListener('mouseleave', () => {
        const megaMenu = trigger.querySelector('.mega-menu');
        if (megaMenu) {
            megaMenu.classList.remove('open');
        }
    });
});

// ===== CART DRAWER =====
function toggleCart() {
    const cartDrawer = document.querySelector('.cart-drawer');
    const cartOverlay = document.querySelector('.cart-overlay');
    
    if (cartDrawer && cartOverlay) {
        cartDrawer.classList.toggle('open');
        cartOverlay.classList.toggle('open');
        document.body.style.overflow = cartDrawer.classList.contains('open') ? 'hidden' : '';
        
        // Load cart items when opening
        if (cartDrawer.classList.contains('open')) {
            loadCartItems();
        }
    } else {
        console.error('Cart drawer or overlay not found');
    }
}

// Initialize cart event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const cartClose = document.querySelector('.cart-close');
    const cartOverlay = document.querySelector('.cart-overlay');
    
    if (cartClose) {
        cartClose.addEventListener('click', toggleCart);
    }
    
    if (cartOverlay) {
        cartOverlay.addEventListener('click', toggleCart);
    }
});

// ===== LOAD CART ITEMS =====
function loadCartItems() {
    fetch('/cart/summary/')
        .then(response => response.json())
        .then(data => {
            const count = data.total_items || data.cart_count || 0;
            updateCartCount(count);
            loadCartItemsDetails();
        })
        .catch(error => {
            console.error('Error loading cart:', error);
            // Show empty cart on error
            document.getElementById('empty-cart-message').style.display = 'block';
            document.getElementById('cart-items-list').style.display = 'none';
        });
}

function loadCartItemsDetails() {
    fetch('/cart/view/')
        .then(response => response.text())
        .then(html => {
            // Parse the HTML response to get cart items
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const cartItems = doc.querySelectorAll('.cart-item');
            const cartItemsList = document.getElementById('cart-items-list');
            const emptyCartMessage = document.getElementById('empty-cart-message');
            const cartFooter = document.getElementById('cart-footer');
            
            if (cartItems.length > 0) {
                // Update cart drawer with items
                const cartItemsHtml = Array.from(cartItems).map(item => {
                    // Simplify the cart item for drawer display
                    const name = item.querySelector('h3')?.textContent || 'Product';
                    const price = item.querySelector('.text-red-500')?.textContent || '₹0';
                    const quantity = item.querySelector('.text-center')?.textContent || '1';
                    const image = item.querySelector('img')?.src || '';
                    
                    return `
                        <div class="flex items-center gap-4 py-4 border-b border-white/10">
                            <div class="w-16 h-16 bg-gray-700 rounded-lg overflow-hidden flex-shrink-0">
                                ${image ? `<img src="${image}" alt="${name}" class="w-full h-full object-cover">` : 
                                '<div class="w-full h-full bg-gray-600 flex items-center justify-center"><svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg></div>'}
                            </div>
                            <div class="flex-1">
                                <h4 class="font-semibold text-white text-sm">${name}</h4>
                                <p class="text-red-500 font-bold">${price}</p>
                                <p class="text-gray-400 text-xs">Qty: ${quantity}</p>
                            </div>
                        </div>
                    `;
                }).join('');
                
                cartItemsList.innerHTML = cartItemsHtml;
                emptyCartMessage.style.display = 'none';
                cartFooter.style.display = 'block';
                
                // Update totals
                const subtotal = doc.querySelector('[class*="get_total_price"]')?.textContent || '₹0';
                document.getElementById('cart-subtotal').textContent = subtotal;
                
                // Calculate total with shipping and GST
                const subtotalNum = parseFloat(subtotal.replace('₹', '')) || 0;
                const shipping = 99;
                const gst = subtotalNum * 0.18;
                const total = subtotalNum + shipping + gst;
                
                document.getElementById('cart-shipping').textContent = `₹${shipping.toFixed(2)}`;
                document.getElementById('cart-gst').textContent = `₹${gst.toFixed(2)}`;
                document.getElementById('cart-total').textContent = `₹${total.toFixed(2)}`;
            } else {
                // Show empty cart
                emptyCartMessage.style.display = 'block';
                cartItemsList.style.display = 'none';
                cartFooter.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error loading cart items:', error);
            document.getElementById('empty-cart-message').style.display = 'block';
            document.getElementById('cart-items-list').style.display = 'none';
        });
}

// ===== 3D TILT EFFECT =====
function initTiltEffect() {
    const tiltCards = document.querySelectorAll('.tilt-card');
    
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });
}

initTiltEffect();

// ===== MAGNETIC BUTTONS =====
function initMagneticButtons() {
    const magneticBtns = document.querySelectorAll('.magnetic-btn');
    
    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        });
        
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate(0, 0)';
        });
    });
}

initMagneticButtons();

// ===== COUNTDOWN TIMER =====
function initCountdown() {
    const countdownElements = document.querySelectorAll('.countdown-timer');
    
    countdownElements.forEach(countdown => {
        const targetDate = countdown.dataset.date;
        if (!targetDate) return;
        
        const target = new Date(targetDate).getTime();
        
        function updateCountdown() {
            const now = new Date().getTime();
            const distance = target - now;
            
            if (distance < 0) {
                countdown.innerHTML = '<div class="text-2xl font-bold text-gold-500">Sale Ended</div>';
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            countdown.innerHTML = `
                <div class="countdown-item">
                    <div class="countdown-number">${days}</div>
                    <div class="countdown-label">Days</div>
                </div>
                <div class="countdown-item">
                    <div class="countdown-number">${hours}</div>
                    <div class="countdown-label">Hours</div>
                </div>
                <div class="countdown-item">
                    <div class="countdown-number">${minutes}</div>
                    <div class="countdown-label">Minutes</div>
                </div>
                <div class="countdown-item">
                    <div class="countdown-number">${seconds}</div>
                    <div class="countdown-label">Seconds</div>
                </div>
            `;
        }
        
        updateCountdown();
        setInterval(updateCountdown, 1000);
    });
}

initCountdown();

// ===== LIVE SEARCH =====
const searchInput = document.querySelector('.mega-search input');
const searchResults = document.querySelector('.search-results');

if (searchInput && searchResults) {
    let debounceTimer;
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        const query = e.target.value;
        
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }
        
        debounceTimer = setTimeout(() => {
            fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.results && data.results.length > 0) {
                        searchResults.innerHTML = data.results.map(item => `
                            <a href="${item.url}" class="search-result-item flex items-center gap-4 p-4 hover:bg-white/5 transition">
                                <img src="${item.image}" alt="${item.name}" class="w-16 h-16 object-cover rounded-lg">
                                <div>
                                    <h4 class="font-semibold">${item.name}</h4>
                                    <p class="text-sm text-gray-400">${item.category}</p>
                                    <p class="text-gold-500 font-bold">₹${item.price}</p>
                                </div>
                            </a>
                        `).join('');
                        searchResults.style.display = 'block';
                    } else {
                        searchResults.innerHTML = '<div class="p-4 text-center text-gray-400">No results found</div>';
                        searchResults.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Search error:', error);
                });
        }, 300);
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', (e) => {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.style.display = 'none';
        }
    });
}

// ===== TOGGLE SEARCH =====
function toggleSearch() {
    const searchModal = document.getElementById('search-modal');
    if (searchModal) {
        searchModal.classList.toggle('hidden');
        if (!searchModal.classList.contains('hidden')) {
            document.getElementById('search-input').focus();
        }
    }
}

// ===== VOICE SEARCH =====
const voiceSearchBtn = document.querySelector('.voice-search-btn');
if (voiceSearchBtn && 'webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    
    voiceSearchBtn.addEventListener('click', () => {
        recognition.start();
        voiceSearchBtn.classList.add('listening');
    });
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (searchInput) {
            searchInput.value = transcript;
            searchInput.dispatchEvent(new Event('input'));
        }
        voiceSearchBtn.classList.remove('listening');
    };
    
    recognition.onerror = () => {
        voiceSearchBtn.classList.remove('listening');
    };
    
    recognition.onend = () => {
        voiceSearchBtn.classList.remove('listening');
    };
}

// ===== QUICK VIEW MODAL =====
const quickViewBtns = document.querySelectorAll('.quick-view-btn');
const quickViewModal = document.querySelector('.quick-view-modal');

quickViewBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const productId = btn.dataset.productId;
        
        // Fetch product details
        fetch(`/api/products/${productId}/`)
            .then(response => response.json())
            .then(data => {
                // Populate modal with product data
                const modalContent = quickViewModal.querySelector('.modal-content');
                modalContent.innerHTML = `
                    <div class="grid md:grid-cols-2 gap-8">
                        <div>
                            <img src="${data.main_image}" alt="${data.name}" class="w-full rounded-lg">
                        </div>
                        <div>
                            <h2 class="text-3xl font-bold mb-4">${data.name}</h2>
                            <p class="text-gold-500 text-2xl font-bold mb-4">₹${data.sale_price || data.regular_price}</p>
                            <p class="text-gray-300 mb-6">${data.short_description}</p>
                            <button class="btn-premium bg-gradient-to-r from-gold-500 to-gold-600 text-black px-8 py-3 rounded-full font-semibold">
                                Add to Cart
                            </button>
                        </div>
                    </div>
                `;
                quickViewModal.classList.add('open');
                document.body.style.overflow = 'hidden';
            });
    });
});

// Close modal
const modalClose = document.querySelector('.modal-close');
if (modalClose) {
    modalClose.addEventListener('click', () => {
        quickViewModal.classList.remove('open');
        document.body.style.overflow = '';
    });
}

// ===== ADD TO CART =====
document.addEventListener('DOMContentLoaded', function() {
    const addToCartBtns = document.querySelectorAll('.add-to-cart-btn');
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = btn.dataset.productId || 1; // Default to product ID 1 for demo
            const quantity = btn.dataset.quantity || 1;
            
            // Add to cart via API
            fetch('/cart/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCsrfToken()
                },
                body: `product_id=${productId}&quantity=${quantity}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('Product added to cart!', 'success');
                    updateCartCount(data.cart_count);
                    // Open cart drawer
                    toggleCart();
                } else {
                    showToast(data.message || 'Error adding to cart', 'error');
                }
            })
            .catch(error => {
                showToast('Error adding to cart', 'error');
            });
        });
    });
});

// ===== TOAST NOTIFICATIONS =====
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// ===== UPDATE CART COUNT =====
function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        element.textContent = count;
    });
}

// ===== GET CSRF TOKEN =====
function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : '';
}

// ===== TABS =====
const tabs = document.querySelectorAll('.tab');
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const tabGroup = tab.closest('.tabs-container');
        const tabId = tab.dataset.tab;
        
        // Remove active class from all tabs in group
        tabGroup.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tabGroup.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked tab
        tab.classList.add('active');
        document.getElementById(tabId).classList.add('active');
    });
});

// ===== ACCORDION =====
const accordionHeaders = document.querySelectorAll('.accordion-header');
accordionHeaders.forEach(header => {
    header.addEventListener('click', () => {
        const content = header.nextElementSibling;
        const icon = header.querySelector('.accordion-icon');
        
        // Close other accordions
        const allContents = document.querySelectorAll('.accordion-content');
        const allIcons = document.querySelectorAll('.accordion-icon');
        
        allContents.forEach(c => {
            if (c !== content) c.classList.remove('open');
        });
        allIcons.forEach(i => {
            if (i !== icon) i.style.transform = 'rotate(0deg)';
        });
        
        // Toggle current accordion
        content.classList.toggle('open');
        icon.style.transform = content.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
    });
});

// ===== IMAGE GALLERY =====
function initImageGallery() {
    const mainImage = document.querySelector('.main-product-image');
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    
    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', () => {
                // Update main image
                mainImage.src = thumb.src;
                
                // Update active thumbnail
                thumbnails.forEach(t => t.classList.remove('active'));
                thumb.classList.add('active');
            });
        });
    }
}

initImageGallery();

// ===== PRODUCT ZOOM =====
function initProductZoom() {
    const zoomContainer = document.querySelector('.zoom-container');
    const zoomImage = zoomContainer?.querySelector('img');
    
    if (zoomContainer && zoomImage) {
        zoomContainer.addEventListener('mousemove', (e) => {
            const rect = zoomContainer.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            zoomImage.style.transformOrigin = `${x}% ${y}%`;
            zoomImage.style.transform = 'scale(2)';
        });
        
        zoomContainer.addEventListener('mouseleave', () => {
            zoomImage.style.transform = 'scale(1)';
        });
    }
}

initProductZoom();

// ===== PINCODE CHECKER =====
const pincodeInput = document.querySelector('.pincode-input');
const checkPincodeBtn = document.querySelector('.check-pincode-btn');
const pincodeResult = document.querySelector('.pincode-result');

if (checkPincodeBtn && pincodeInput) {
    checkPincodeBtn.addEventListener('click', () => {
        const pincode = pincodeInput.value;
        
        if (pincode.length !== 6) {
            pincodeResult.innerHTML = '<span class="text-red-500">Please enter a valid 6-digit pincode</span>';
            return;
        }
        
        fetch(`/api/check-pincode/?pincode=${pincode}`)
            .then(response => response.json())
            .then(data => {
                if (data.available) {
                    pincodeResult.innerHTML = `
                        <span class="text-green-500">
                            ✓ Available! Delivery in ${data.delivery_days} days
                        </span>
                    `;
                } else {
                    pincodeResult.innerHTML = `
                        <span class="text-red-500">
                            ✗ Not available in this area
                        </span>
                    `;
                }
            })
            .catch(error => {
                pincodeResult.innerHTML = '<span class="text-red-500">Error checking pincode</span>';
            });
    });
}

// ===== LAZY LOADING =====
if ('IntersectionObserver' in window) {
    const lazyImages = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
}

// ===== WHATSAPP ORDER =====
const whatsappBtn = document.querySelector('.whatsapp-order-btn');
if (whatsappBtn) {
    whatsappBtn.addEventListener('click', () => {
        const productName = whatsappBtn.dataset.product;
        const message = `Hi, I'm interested in ordering: ${productName}`;
        const whatsappUrl = `https://wa.me/919876543210?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');
    });
}

// ===== LIVE CHAT =====
const liveChatBtn = document.querySelector('.live-chat-btn');
const liveChatWidget = document.querySelector('.live-chat-widget');

if (liveChatBtn && liveChatWidget) {
    liveChatBtn.addEventListener('click', () => {
        liveChatWidget.classList.toggle('open');
    });
}

// ===== ORDER TRACKING =====
const trackingForm = document.querySelector('.tracking-form');
if (trackingForm) {
    trackingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const orderId = trackingForm.querySelector('#order-id').value;
        
        fetch(`/api/track-order/${orderId}/`)
            .then(response => response.json())
            .then(data => {
                const trackingResult = document.querySelector('.tracking-result');
                if (data.success) {
                    trackingResult.innerHTML = `
                        <div class="bg-white/5 rounded-lg p-6">
                            <h3 class="text-xl font-bold mb-4">Order #${data.order_id}</h3>
                            <div class="space-y-4">
                                <div class="flex justify-between">
                                    <span>Status:</span>
                                    <span class="text-gold-500">${data.status}</span>
                                </div>
                                <div class="flex justify-between">
                                    <span>Estimated Delivery:</span>
                                    <span>${data.estimated_delivery}</span>
                                </div>
                                <div class="tracking-timeline">
                                    ${data.timeline.map(item => `
                                        <div class="timeline-item">
                                            <div class="timeline-date">${item.date}</div>
                                            <div class="timeline-status">${item.status}</div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    `;
                } else {
                    trackingResult.innerHTML = '<div class="text-red-500">Order not found</div>';
                }
            })
            .catch(error => {
                console.error('Tracking error:', error);
            });
    });
}

// ===== NEWSLETTER =====
const newsletterForm = document.querySelector('.newsletter-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input[type="email"]').value;
        
        fetch('/api/newsletter/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Thank you for subscribing!', 'success');
                newsletterForm.reset();
            } else {
                showToast(data.message || 'Error subscribing', 'error');
            }
        })
        .catch(error => {
            showToast('Error subscribing', 'error');
        });
    });
}

// ===== WISHLIST =====
document.addEventListener('DOMContentLoaded', function() {
    const wishlistBtns = document.querySelectorAll('.wishlist-btn');
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const productId = btn.dataset.productId || 1;
            
            fetch('/wishlist/add/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCsrfToken()
                },
                body: `product_id=${productId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast('Product added to wishlist!', 'success');
                    updateWishlistCount(data.total_items);
                } else {
                    showToast(data.message || 'Error adding to wishlist', 'error');
                }
            })
            .catch(error => {
                showToast('Error adding to wishlist', 'error');
            });
        });
    });
});

// ===== DARK MODE TOGGLE =====
const darkModeToggle = document.querySelector('.dark-mode-toggle');
if (darkModeToggle) {
    darkModeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
    });
    
    // Check saved preference
    if (localStorage.getItem('darkMode') === 'false') {
        document.documentElement.classList.remove('dark');
    }
}

// ===== INITIALIZE =====
document.addEventListener('DOMContentLoaded', () => {
    // Load cart count on page load
    loadCartCount();
    
    // Reinitialize animations after dynamic content loads
    ScrollTrigger.refresh();
});

// ===== LOAD CART COUNT =====
function loadCartCount() {
    fetch('/cart/summary/')
        .then(response => response.json())
        .then(data => {
            const count = data.total_items || data.cart_count || 0;
            updateCartCount(count);
        })
        .catch(error => {
            console.error('Error loading cart count:', error);
        });
}

// Performance optimization: Debounce resize events
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        ScrollTrigger.refresh();
    }, 250);
});