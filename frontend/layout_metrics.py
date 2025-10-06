class LayoutMetrics:
    def __init__(self, layout_data):
        self.data = layout_data
        self.calculate_metrics()

    def calculate_metrics(self):
        # Basic habitat metrics
        self.total_height = self.data['habitat_dimensions']['total_height_m']
        self.base_diameter = self.data['habitat_dimensions']['cylindrical_base_diameter_m']
        self.total_levels = len(self.data.get('levels', []))
        
        # Module statistics
        self.total_modules = len(self.data.get('modules', []))
        self.modules_by_category = self._count_modules_by_category()
        
        # Level statistics
        self.level_metrics = self._calculate_level_metrics()
        
        # Violation statistics
        self.violation_stats = self._analyze_violations()

    def _count_modules_by_category(self):
        categories = {'CLEAN': 0, 'DIRTY': 0, 'QUIET': 0, 'NOISY': 0, 'NEUTRAL': 0}
        for module in self.data.get('modules', []):
            category = module.get('category', 'NEUTRAL')
            categories[category] += 1
        return categories

    def _calculate_level_metrics(self):
        level_metrics = []
        for level in self.data.get('levels', []):
            metrics = {
                'height_range': f"{level['min_z']:.1f}m - {level['max_z']:.1f}m",
                'module_count': len(level['modules']),
                'total_area': sum(mod.get('scale', {}).get('x', 0) * mod.get('scale', {}).get('y', 0) 
                                for mod in level['modules']),
                'modules': [mod['name'] for mod in level['modules']]
            }
            level_metrics.append(metrics)
        return level_metrics

    def _analyze_violations(self):
        violation_summary = self.data.get('violation_summary', {})
        total_violations = sum(v.get('count', 0) for v in violation_summary.values())
        max_severity = max((v.get('max_severity', 0) for v in violation_summary.values()), default=0)
        
        return {
            'total_count': total_violations,
            'max_severity': max_severity,
            'by_type': violation_summary
        }

    def get_summary_text(self):
        """Returns a formatted summary of the layout metrics"""
        return f"""Habitat Overview:
• Total Height: {self.total_height:.1f}m
• Base Diameter: {self.base_diameter:.1f}m
• Number of Levels: {self.total_levels}
• Total Modules: {self.total_modules}

Module Distribution:
• Clean Areas: {self.modules_by_category['CLEAN']}
• Dirty Areas: {self.modules_by_category['DIRTY']}
• Quiet Areas: {self.modules_by_category['QUIET']}
• Noisy Areas: {self.modules_by_category['NOISY']}
• Neutral Areas: {self.modules_by_category['NEUTRAL']}

Layout Issues:
• Total Violations: {self.violation_stats['total_count']}
• Maximum Severity: {self.violation_stats['max_severity']:.2f}
"""