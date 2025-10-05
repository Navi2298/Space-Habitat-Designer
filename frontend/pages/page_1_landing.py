from nicegui import ui

def landing_page():
    """Defines the content and layout for the landing page."""
    
    # --- 1. Custom CSS for Animated Background (No GSAP/ScrollTrigger imports) ---
    ui.add_head_html("""
        <style>
            /* Base dark background for the body */
            body { 
                background-color: #04040A; 
                /* Allow scrolling now that we have extra content */
                overflow-y: auto; 
                overflow-x: hidden;
            }

            /* Define the blinking animation for the stars */
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.2; } /* Subtler blink */
            }

            /* Container for the stars - covers the full screen */
            .star-field {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -10; 
            }

            /* The actual star element - a small white dot with a subtle blue glow */
            .star {
                position: absolute;
                background: #FFFFFF; 
                border-radius: 50%;
                box-shadow: 0 0 5px 1px rgba(66, 165, 245, 0.5); /* Blue glow */
                animation-name: blink;
                animation-timing-function: linear;
                animation-iteration-count: infinite;
            }
            
            /* Class to ensure the content is centered over the background */
            .content-container {
                z-index: 10;
                position: relative;
            }

            /* --- Logo Positioning --- */
            /* NASA Logo: Top Left */
            .hackathon-logo {
                position: fixed;
                top: 1rem;    /* Positioned at the top */
                left: 1rem;   /* Positioned at the left */
                width: 200px; /* Size */
                opacity: 0.9; 
                z-index: 100;
            }
            
            /* Team Logo (NEW): Top Right */
            .team-logo {
                position: fixed;
                top: 1rem;    /* Positioned at the top */
                right: 1rem;  /* Positioned at the right */
                width: 120px; /* Size, slightly smaller than the NASA logo */
                opacity: 0.9;
                z-index: 100;
            }

            /* Custom class for page content column - now simply stacked content */
            .main-page-column {
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
            }
        </style>
        
        <!-- Star Field Container -->
        <div id="star-field" class="star-field"></div>
        
        <!-- Star Generation Script -->
        <script>
            function createStar(size, duration) {
                const star = document.createElement('div');
                star.classList.add('star');
                
                // Randomly position the star across the screen
                const x = Math.random() * 100;
                const y = Math.random() * 100;

                star.style.left = x + 'vw';
                star.style.top = y + 'vh';
                star.style.width = size + 'px';
                star.style.height = size + 'px';

                // Randomize blink speed and delay
                star.style.animationDuration = (duration + (Math.random() * 2)) + 's';
                star.style.animationDelay = (Math.random() * 5) + 's';
                
                return star;
            }

            const starField = document.getElementById('star-field');
            const numStars = 200; // Total number of stars

            for (let i = 0; i < numStars; i++) {
                // Generate stars with varying sizes and base animation speeds
                let size = (Math.random() * 3) + 1.0; 
                let duration = 3 + (Math.random() * 4); // Duration between 3s and 7s
                starField.appendChild(createStar(size, duration));
            }
        </script>
    """)

    # --- 2. Hackathon Logo (Top Left) ---
    ui.image('Images/NASA-SPACE-APPS-Logo.png').classes('hackathon-logo')

    # --- 2.1. Team Logo (Top Right) ---
    ui.image('Images/MyHab_logo.png').classes('team-logo')

    # --- 3. Main Content Container ---
    # We use a standard column here, and let the inner elements define their own width (max-w-2xl) or full width (w-screen).
    with ui.column().classes('main-page-column w-screen p-8 pt-20 pb-16 gap-10'): 
        
        # --- A. Primary Information and Action Card (Centered, max-width) ---
        # Card width is set to max-w-2xl for the original, focused size.
        with ui.column().classes('p-10 bg-gray-900/90 backdrop-blur-md rounded-3xl shadow-2xl max-w-2xl border border-blue-700/50 transition-all duration-500 hover:shadow-blue-500/80 content-container items-center'):
            
            # Title 
            ui.label('MyHab').classes('text-5xl font-extrabold text-white leading-tight tracking-wider transition-colors duration-300')
            # Subtitle Updated
            ui.label('Layout Designer for Lunar & Martian Missions.').classes('text-xl text-blue-300 font-light mt-1 mb-6')
            
            ui.separator().classes('w-full border-t-2 border-blue-600/70')
            
            # Description
            with ui.markdown(
                """
                The **Habitat Blueprint Designer** is a professional-grade visual tool engineered to **accelerate the preliminary design phase** of crewed lunar and Martian habitats. Recognizing the complexity of integrating diverse mission functions within stringent launch and deployment envelopes, this application offers **rapid prototyping** powered by mission constraints.
                
                Users define core parameters—such as crew size and mission duration—to generate an initial layout compliant with required functional volumes. Leverage the interactive 2D editor to **dynamically partition the habitat** and receive **instant, rule-based feedback** on sizing and placement, ensuring rigorous adherence to critical mission specifications.
                """
            ).classes('text-base text-gray-200 text-center space-y-4'):
                # Custom styling for elements inside the markdown for better contrast
                ui.run_javascript(
                    """
                    document.querySelectorAll('.nicegui-markdown strong').forEach(s => {
                        s.classList.add('text-yellow-300');
                    });
                    """
                )
            
            # Action button
            ui.button(
                'Start Designing Now', 
                on_click=lambda: ui.navigate.to('/parameters')
            ).classes('mt-10 w-64 h-14 bg-green-600 hover:bg-green-500 text-xl font-bold text-white shadow-lg shadow-green-500/50 transition-transform transform hover:scale-105 rounded-full')
        
        # --- B. Background Story Data Strip (Full Width) ---
        # This wrapper spans the entire screen width (w-screen) and is centered in the main column (mx-auto).
        with ui.column().classes('w-screen bg-slate-900 py-16 mt-16 shadow-2xl shadow-blue-900/50 items-center'):
            # This inner column ensures the text content itself is centered and has a max width.
            with ui.column().classes('max-w-6xl mx-auto px-8 items-center'):
            
                ui.label('MyHab: Mission Context').classes('text-3xl font-extrabold text-teal-400 mb-6 text-center w-full tracking-wide')

                # Background Story Content
                ui.markdown(
                    """
                    NASA plans to return humans to the **Moon** and enable a sustained presence there through the **Artemis campaign**. The Moon will serve as a proving ground for technologies and operational approaches that will inform future human missions to **Mars**. 
                    
                    Space habitats can potentially support crews on the Moon, in transit to Mars, and on the Martian surface, enabling **longer mission durations**, increased crew sizes, and comprehensive science investigations. Habitat designers must consider not only the structural, manufacturing, and material options but also the constraints imposed by **delivery/deployment methods** (e.g., the capacity of a lunar surface landing system and/or a launch vehicle). Additionally, a space habitat must provide numerous functions to support the required number of crew members for the specified mission duration at the final destination or while in transit.
                    
                    There are generally three different classes of space habitat structures: **metallic habitats** that are launched from Earth in their usable form, **inflatable habitats** that are stowed for launch and deployed at the point of use, and habitats that can be **manufactured on a planetary surface**, potentially from indigenous resources (**in-situ**). The challenge lies in creating a viable concept quickly, as existing tools often require a high level of expertise and significant time to evaluate multiple design options.
                    """
                ).classes('text-lg text-slate-300 text-justify space-y-4')

                # Run JavaScript to apply the yellow/gold color to bold text in the story section
                ui.run_javascript(
                    """
                    document.querySelectorAll('.bg-slate-900 .nicegui-markdown strong').forEach(s => {
                        s.classList.add('text-yellow-400');
                    });
                    """
                )
