
        // Improved Language Switching Function
        function setLanguage(langCode) {
            console.log('Switching to language:', langCode);
            
            // Create form for language switching
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/i18n/setlang/';
            form.style.display = 'none';
            
            // Get CSRF token - try multiple methods
            let csrfToken = null;
            
            // Method 1: From cookie
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrftoken') {
                    csrfToken = decodeURIComponent(value);
                    break;
                }
            }
            
            // Method 2: From existing form
            if (!csrfToken) {
                const existingInput = document.querySelector('[name="csrfmiddlewaretoken"]');
                if (existingInput) {
                    csrfToken = existingInput.value;
                }
            }
            
            // Method 3: From meta tag
            if (!csrfToken) {
                const metaTag = document.querySelector('meta[name="csrf-token"]');
                if (metaTag) {
                    csrfToken = metaTag.getAttribute('content');
                }
            }
            
            // Method 4: From template variable (fallback)
            if (!csrfToken) {
                csrfToken = '{{ csrf_token }}';
            }
            
            console.log('CSRF Token found:', csrfToken ? 'Yes' : 'No');
            
            // Add CSRF token
            const csrfInput = document.createElement('input');
            csrfInput.type = 'hidden';
            csrfInput.name = 'csrfmiddlewaretoken';
            csrfInput.value = csrfToken;
            form.appendChild(csrfInput);
            
            // Add language
            const langInput = document.createElement('input');
            langInput.type = 'hidden';
            langInput.name = 'language';
            langInput.value = langCode;
            form.appendChild(langInput);
            
            // Add next URL - determine current page and switch language
            let currentPath = window.location.pathname;
            let nextUrl;
            
            if (currentPath.startsWith('/en/')) {
                nextUrl = currentPath.replace('/en/', '/' + langCode + '/');
            } else if (currentPath.startsWith('/tr/')) {
                nextUrl = currentPath.replace('/tr/', '/' + langCode + '/');
            } else {
                nextUrl = '/' + langCode + '/landing/';
            }
            
            const nextInput = document.createElement('input');
            nextInput.type = 'hidden';
            nextInput.name = 'next';
            nextInput.value = nextUrl;
            form.appendChild(nextInput);
            
            console.log('Redirecting to:', nextUrl);
            
            // Submit form
            document.body.appendChild(form);
            form.submit();
        }
        
        // Alternative method using fetch (more modern)
        async function setLanguageModern(langCode) {
            console.log('Modern language switch to:', langCode);
            
            try {
                // Get CSRF token
                let csrfToken = null;
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    const [name, value] = cookie.trim().split('=');
                    if (name === 'csrftoken') {
                        csrfToken = decodeURIComponent(value);
                        break;
                    }
                }
                
                if (!csrfToken) {
                    const existingInput = document.querySelector('[name="csrfmiddlewaretoken"]');
                    if (existingInput) {
                        csrfToken = existingInput.value;
                    }
                }
                
                // Determine next URL
                let currentPath = window.location.pathname;
                let nextUrl;
                
                if (currentPath.startsWith('/en/')) {
                    nextUrl = currentPath.replace('/en/', '/' + langCode + '/');
                } else if (currentPath.startsWith('/tr/')) {
                    nextUrl = currentPath.replace('/tr/', '/' + langCode + '/');
                } else {
                    nextUrl = '/' + langCode + '/landing/';
                }
                
                // Send POST request
                const formData = new FormData();
                formData.append('language', langCode);
                formData.append('next', nextUrl);
                formData.append('csrfmiddlewaretoken', csrfToken);
                
                const response = await fetch('/i18n/setlang/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                    redirect: 'follow'
                });
                
                if (response.ok) {
                    // Redirect to the new language page
                    window.location.href = nextUrl;
                } else {
                    console.error('Language switch failed:', response.status);
                    // Fallback to form submission
                    setLanguage(langCode);
                }
                
            } catch (error) {
                console.error('Modern language switch failed:', error);
                // Fallback to form submission
                setLanguage(langCode);
            }
        }
    