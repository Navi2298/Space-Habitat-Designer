from nicegui import ui

def landing_page():
    """Defines the content and layout for the landing page."""
    
    # --- 1. Custom CSS for Animated Background ---
    ui.add_head_html("""
        <style>
            /* Base dark background for the body */
            body { 
                background-color: #04040A; 
                overflow: hidden; 
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
                // UPDATED: Changed size from (0.5 to 2.5) to (1.0 to 4.0) for larger stars
                let size = (Math.random() * 3) + 1.0; 
                let duration = 3 + (Math.random() * 4); // Duration between 3s and 7s
                starField.appendChild(createStar(size, duration));
            }
        </script>
    """)

    # 2. Main Content Container
    with ui.row().classes('w-screen h-screen items-center justify-center'):
        with ui.column().classes('p-10 bg-gray-900/90 backdrop-blur-md rounded-3xl shadow-2xl max-w-2xl border border-blue-700/50 transition-all duration-500 hover:shadow-blue-500/80 content-container items-center'):
            
            # Title
            ui.label('Artemis Mission Habitat Designer').classes('text-5xl font-extrabold text-white leading-tight tracking-wider transition-colors duration-300')
            ui.label('The blueprint for humanity\'s next home.').classes('text-xl text-blue-300 font-light mt-1 mb-6')
            
            ui.separator().classes('w-full border-t-2 border-blue-600/70')
            
            # Description
            with ui.markdown(
                """
                ### Purpose & Solution
                This application helps space architects **rapidly prototype** crewed habitat designs for lunar and Martian missions. 
                
                By defining mission parameters, the system instantly generates a compliant initial layout based on required living volumes. 
                
                **The solution?** Rapid iteration, instant constraint feedback, and a tool that keeps your design grounded in real-world mission needs.
                """
            ).classes('text-lg text-gray-200 text-center space-y-4'):
                # Custom styling for elements inside the markdown for better contrast
                ui.run_javascript(
                    """
                    document.querySelectorAll('.nicegui-markdown h3').forEach(h => {
                        h.classList.add('text-blue-400', 'font-extrabold', 'mt-4');
                    });
                    document.querySelectorAll('.nicegui-markdown strong').forEach(s => {
                        s.classList.add('text-yellow-300');
                    });
                    """
                )
            
            # Action button
            ui.button('Start Designing Now', on_click=lambda: ui.open('/parameters')).classes('mt-10 w-64 h-14 bg-green-600 hover:bg-green-500 text-xl font-bold text-white shadow-lg shadow-green-500/50 transition-transform transform hover:scale-105 rounded-full')
