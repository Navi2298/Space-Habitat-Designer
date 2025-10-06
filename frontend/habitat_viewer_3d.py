from nicegui import ui
import three
import json

class HabitatViewer3D:
    def __init__(self, layout_data):
        self.layout_data = layout_data
        self.scene = None
        self.camera = None
        self.renderer = None
        
    def setup_scene(self, container):
        # Create Three.js scene
        self.scene = three.Scene()
        
        # Add camera
        self.camera = three.PerspectiveCamera(75, aspect_ratio=1.0)
        self.camera.position = (10, 10, 10)
        self.camera.look_at((0, 0, 0))
        
        # Add lighting
        ambient_light = three.AmbientLight(color='white', intensity=0.5)
        directional_light = three.DirectionalLight(color='white', intensity=0.8)
        directional_light.position = (5, 5, 5)
        self.scene.add(ambient_light)
        self.scene.add(directional_light)
        
        # Create habitat boundary cylinder
        radius = self.layout_data['habitat_dimensions']['cylindrical_base_diameter_m'] / 2
        height = self.layout_data['habitat_dimensions']['total_height_m']
        cylinder = three.Mesh(
            geometry=three.CylinderGeometry(radius=radius, height=height),
            material=three.MeshStandardMaterial(
                color='#cccccc',
                transparent=True,
                opacity=0.3,
                wireframe=True
            )
        )
        self.scene.add(cylinder)
        
        # Add modules
        for module in self.layout_data['modules']:
            self.add_module(module)
        
        # Create renderer
        self.renderer = three.Renderer(antialias=True)
        container.clear()
        with container:
            ui.add_head_html('''
                <style>
                    .three-scene { width: 100%; height: 100%; }
                </style>
            ''')
            self.renderer.classes('three-scene')
        
        # Add orbit controls
        controls = three.OrbitControls(controlling=self.camera, container=container.id)
        
        # Start animation loop
        def update():
            self.renderer.render(self.scene, self.camera)
            
        ui.timer(interval=1/60, callback=update)
    
    def add_module(self, module):
        # Create module geometry
        pos = module['position']
        scale = module.get('scale', {'x': 1, 'y': 1, 'z': 1})
        
        # Determine color based on category and violations
        color = {
            'CLEAN': '#90EE90',
            'DIRTY': '#FFB6C1',
            'QUIET': '#E6E6FA',
            'NOISY': '#FFA07A',
            'NEUTRAL': '#ADD8E6'
        }.get(module.get('category', 'NEUTRAL'))
        
        # Create module mesh
        geometry = three.BoxGeometry(
            width=scale['x'],
            height=scale['z'],  # Note: Y is up in Three.js
            depth=scale['y']
        )
        material = three.MeshStandardMaterial(color=color)
        mesh = three.Mesh(geometry=material)
        
        # Position module
        mesh.position = (pos['x'], pos['z'], pos['y'])  # Convert coordinate systems
        
        # Add to scene
        self.scene.add(mesh)
        
        # Add module label
        self.add_module_label(module, mesh.position)