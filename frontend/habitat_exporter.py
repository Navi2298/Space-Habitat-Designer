import svgwrite
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
import json
import os

class HabitatExporter:
    def __init__(self, layout_data):
        self.layout_data = layout_data
        
    def export_svg(self, filepath):
        """Export the current view as an SVG file"""
        # Create SVG document
        dwg = svgwrite.Drawing(filepath, profile='tiny', size=('800px', '600px'))
        
        # Add title
        dwg.add(dwg.text('Habitat Layout', insert=(400, 30), 
                        text_anchor='middle', font_size=20))
        
        # Create main group with center transform
        main_group = dwg.g(transform='translate(400,300)')
        
        # Add habitat boundary
        radius = self.layout_data['habitat_dimensions']['cylindrical_base_diameter_m'] / 2
        main_group.add(dwg.circle(center=(0, 0), r=radius,
                                fill='none', stroke='black', stroke_width=2))
        
        # Add modules
        for module in self.layout_data['modules']:
            self._add_module_to_svg(main_group, module)
        
        # Add group to drawing
        dwg.add(main_group)
        
        # Save SVG file
        dwg.save()
        
    def _add_module_to_svg(self, group, module):
        """Add a module to the SVG group"""
        pos = module['position']
        scale = module.get('scale', {'x': 1, 'y': 1, 'z': 1})
        
        # Determine color based on category
        color = {
            'CLEAN': '#90EE90',
            'DIRTY': '#FFB6C1',
            'QUIET': '#E6E6FA',
            'NOISY': '#FFA07A',
            'NEUTRAL': '#ADD8E6'
        }.get(module.get('category', 'NEUTRAL'))
        
        # Create module rectangle
        x, y = pos['x'] - scale['x']/2, pos['y'] - scale['y']/2
        group.add(group.rect((x, y), (scale['x'], scale['y']),
                           fill=color, stroke='black', stroke_width=1))
        
        # Add module label
        group.add(group.text(module['name'],
                           insert=(pos['x'], pos['y']),
                           text_anchor='middle',
                           dominant_baseline='middle',
                           font_size=12))
        
    def export_pdf(self, filepath):
        """Export the current view as a PDF file"""
        # Create PDF canvas
        c = canvas.Canvas(filepath, pagesize=landscape(letter))
        width, height = landscape(letter)
        
        # Add title
        c.setFont("Helvetica-Bold", 24)
        c.drawString(width/2 - 100, height - 50, "Habitat Layout")
        
        # Add date and basic info
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Total Modules: {len(self.layout_data['modules'])}")
        
        # Draw habitat boundary
        c.translate(width/2, height/2)  # Move to center
        radius = self.layout_data['habitat_dimensions']['cylindrical_base_diameter_m'] * 20  # Scale for PDF
        c.circle(0, 0, radius)
        
        # Draw modules
        for module in self.layout_data['modules']:
            self._add_module_to_pdf(c, module)
        
        # Add violations summary if any exist
        total_violations = sum(len(m.get('violations', [])) for m in self.layout_data['modules'])
        if total_violations > 0:
            c.translate(-width/2, -height/2)  # Reset translation
            c.setFont("Helvetica-Bold", 14)
            y = 100  # Start position for violations list
            c.drawString(50, y, "Violations Summary:")
            c.setFont("Helvetica", 12)
            for module in self.layout_data['modules']:
                if module.get('violations'):
                    y -= 20
                    c.drawString(70, y, f"{module['name']}: {len(module['violations'])} violation(s)")
        
        # Save PDF
        c.save()
        
    def _add_module_to_pdf(self, canvas, module):
        """Add a module to the PDF canvas"""
        pos = module['position']
        scale = module.get('scale', {'x': 1, 'y': 1, 'z': 1})
        
        # Scale positions for PDF (multiply by 20 for better visibility)
        x, y = pos['x'] * 20, pos['y'] * 20
        width, height = scale['x'] * 20, scale['y'] * 20
        
        # Draw module rectangle
        canvas.rect(x - width/2, y - height/2, width, height)
        
        # Add module label
        canvas.setFont("Helvetica", 8)
        canvas.drawString(x - len(module['name'])*2, y, module['name'])