from nicegui import ui
import json
import os
from pathlib import Path
import math

class ResultPage:
    def __init__(self):
        self.current_view = 'top'  # Can be 'top', 'side', or '3d'
        self.layout_data = None
        self.visualization_container = None
        
    def load_layout_data(self):
        try:
            output_path = Path('output/layout_result.json')
            if not output_path.exists():
                ui.notify('No layout data found. Please generate a layout first.')
                return False
                
            with open(output_path, 'r') as f:
                self.layout_data = json.load(f)
            return True
        except Exception as e:
            ui.notify(f'Error loading layout data: {str(e)}')
            return False
            
    def switch_view(self, view_type):
        self.current_view = view_type
        self.update_visualization()
        
    def draw_top_view(self, container):
        if not self.layout_data:
            return
            
        # Get habitat dimensions
        radius = self.layout_data['habitat_dimensions']['cylindrical_base_diameter_m'] / 2
        
        # Create SVG for top view
        svg_size = 600
        scale_factor = (svg_size * 0.8) / (radius * 2)  # Leave some margin
        
        svg = f'''
        <svg width="{svg_size}" height="{svg_size}" viewBox="0 0 {svg_size} {svg_size}">
            <defs>
                <!-- Define patterns for different shell layers -->
                <pattern id="structuralPattern" patternUnits="userSpaceOnUse" width="10" height="10">
                    <circle cx="5" cy="5" r="1" fill="#666"/>
                </pattern>
                <pattern id="insulationPattern" patternUnits="userSpaceOnUse" width="8" height="8">
                    <path d="M0 0h8v8h-8z" fill="#f0f0f0"/>
                    <path d="M0 0l8 8M8 0l-8 8" stroke="#ddd" stroke-width="1"/>
                </pattern>
            </defs>
            <g transform="translate({svg_size/2}, {svg_size/2})">
                <!-- Shell layers -->
                <circle cx="0" cy="0" r="{radius * scale_factor}" 
                        fill="url(#structuralPattern)" stroke="black" stroke-width="2"/>
                <circle cx="0" cy="0" r="{(radius - 0.5) * scale_factor}" 
                        fill="url(#insulationPattern)" stroke="#999" stroke-width="1"/>
                <circle cx="0" cy="0" r="{(radius - 0.8) * scale_factor}" 
                        fill="white" stroke="#666" stroke-width="1"/>
        '''
        
        # Draw modules
        for module in self.layout_data['modules']:
            x = module['position']['x'] * scale_factor
            y = module['position']['y'] * scale_factor
            width = module.get('scale', {}).get('x', 1) * scale_factor
            height = module.get('scale', {}).get('y', 1) * scale_factor
            
            # Determine color based on category
            color = {
                'CLEAN': '#90EE90',
                'DIRTY': '#FFB6C1',
                'QUIET': '#E6E6FA',
                'NOISY': '#FFA07A',
                'NEUTRAL': '#ADD8E6'
            }.get(module.get('category', 'NEUTRAL'))
            
            # Add module rectangle
            svg += f'''
                <g class="module" data-name="{module['name']}">
                    <rect x="{x - width/2}" y="{y - height/2}" 
                          width="{width}" height="{height}"
                          fill="{color}" stroke="black" stroke-width="1"/>
                    <text x="{x}" y="{y}" text-anchor="middle" 
                          dominant-baseline="middle" font-size="12">
                        {module['name']}
                    </text>
                </g>
            '''
        
        svg += '''
            </g>
        </svg>
        '''
        
        container.clear()
        with container:
            ui.html(svg).classes('w-full h-full')
            
    def draw_side_view(self, container):
        if not self.layout_data:
            return
            
        # Get habitat dimensions
        width = self.layout_data['habitat_dimensions']['cylindrical_base_diameter_m']
        height = self.layout_data['habitat_dimensions']['total_height_m']
        
        # Create SVG for side view
        svg_width = 600
        svg_height = 400
        scale_x = (svg_width * 0.8) / width
        scale_y = (svg_height * 0.8) / height
        scale_factor = min(scale_x, scale_y)
        
        svg = f'''
        <svg width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">
            <defs>
                <!-- Define patterns for different shell layers -->
                <pattern id="structuralPatternSide" patternUnits="userSpaceOnUse" width="10" height="10">
                    <circle cx="5" cy="5" r="1" fill="#666"/>
                </pattern>
                <pattern id="insulationPatternSide" patternUnits="userSpaceOnUse" width="8" height="8">
                    <path d="M0 0h8v8h-8z" fill="#f0f0f0"/>
                    <path d="M0 0l8 8M8 0l-8 8" stroke="#ddd" stroke-width="1"/>
                </pattern>
            </defs>
            <g transform="translate({svg_width/2}, {svg_height/2})">
                <!-- Shell layers -->
                <!-- Outer structural shell -->
                <rect x="{-width * scale_factor/2}" y="{-height * scale_factor/2}" 
                      width="{width * scale_factor}" height="{height * scale_factor}"
                      fill="url(#structuralPatternSide)" stroke="black" stroke-width="2"/>
                
                <!-- Middle insulation layer -->
                <rect x="{(-width + 1) * scale_factor/2}" y="{(-height + 1) * scale_factor/2}" 
                      width="{(width - 1) * scale_factor}" height="{(height - 1) * scale_factor}"
                      fill="url(#insulationPatternSide)" stroke="#999" stroke-width="1"/>
                
                <!-- Inner habitable space -->
                <rect x="{(-width + 1.6) * scale_factor/2}" y="{(-height + 1.6) * scale_factor/2}" 
                      width="{(width - 1.6) * scale_factor}" height="{(height - 1.6) * scale_factor}"
                      fill="white" stroke="#666" stroke-width="1"/>
        '''
        
        # Draw modules
        for module in self.layout_data['modules']:
            x = module['position']['x'] * scale_factor
            z = module['position']['z'] * scale_factor
            width = module.get('scale', {}).get('x', 1) * scale_factor
            height = module.get('scale', {}).get('z', 1) * scale_factor
            
            color = {
                'CLEAN': '#90EE90',
                'DIRTY': '#FFB6C1',
                'QUIET': '#E6E6FA',
                'NOISY': '#FFA07A',
                'NEUTRAL': '#ADD8E6'
            }.get(module.get('category', 'NEUTRAL'))
            
            svg += f'''
                <g class="module" data-name="{module['name']}">
                    <rect x="{x - width/2}" y="{z - height/2}" 
                          width="{width}" height="{height}"
                          fill="{color}" stroke="black" stroke-width="1"/>
                    <text x="{x}" y="{z}" text-anchor="middle" 
                          dominant-baseline="middle" font-size="12">
                        {module['name']}
                    </text>
                </g>
            '''
        
        svg += '''
            </g>
        </svg>
        '''
        
        container.clear()
        with container:
            ui.html(svg).classes('w-full h-full')
            
    def draw_3d_view(self, container):
        # Placeholder for 3D view
        container.clear()
        with container:
            ui.label('3D view will be implemented with Three.js').classes('text-center')
            
    def update_visualization(self):
        if self.visualization_container:
            if self.current_view == 'top':
                self.draw_top_view(self.visualization_container)
            elif self.current_view == 'side':
                self.draw_side_view(self.visualization_container)
            else:  # 3d view
                self.draw_3d_view(self.visualization_container)
                
    def export_pdf(self):
        ui.notify('PDF export functionality coming soon')
        
    def export_svg(self):
        ui.notify('SVG export functionality coming soon')
        
    def __call__(self, router_context=None):
        """Create and display the result page"""
        if not self.load_layout_data():
            return
            
        with ui.column().classes('w-full items-center'):
            ui.label('Habitat Layout Result').classes('text-h4 q-ma-md')
            
            # Add view controls
            with ui.row().classes('w-full justify-center gap-4'):
                ui.button('Top View', on_click=lambda: self.switch_view('top')).classes('bg-blue-500')
                ui.button('Side View', on_click=lambda: self.switch_view('side')).classes('bg-blue-500')
                ui.button('3D View', on_click=lambda: self.switch_view('3d')).classes('bg-blue-500')
            
            # Add visualization container
            self.visualization_container = ui.element('div').classes('w-3/4 aspect-square')
            
            # Add export buttons
            with ui.row().classes('w-full justify-center gap-4 mt-4'):
                ui.button('Export as PDF', on_click=self.export_pdf).classes('bg-green-500')
                ui.button('Export as SVG', on_click=self.export_svg).classes('bg-green-500')
            
            # Initial visualization
            self.update_visualization()

# Create an instance of ResultPage to be used by the router
result_page = ResultPage()
