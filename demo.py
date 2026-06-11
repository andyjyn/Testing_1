#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:34:58 2026

@author: andy
"""

"""
Biogas Upgrading Technology Selector
Run this script to get technology recommendations based on your plant parameters.

How to use:
1. Save this file as biogas_selector.py
2. Run: python biogas_selector.py
3. Answer the prompts
"""

# ============================================================================
# DATA
# ============================================================================

technologies = {
    'Membrane': {
        'min_scale': 50, 'max_scale': 3000,
        'purity_single': 0.95, 'purity_multi': 0.98,
        'cost_small': 0.65, 'cost_medium': 0.72, 'cost_large': 0.80,
        'energy': 0.25, 'slip': 0.02,
    },
    'PSA': {
        'min_scale': 50, 'max_scale': 5000,
        'purity_single': 0.97, 'purity_multi': 0.98,
        'cost_small': 0.70, 'cost_medium': 0.72, 'cost_large': 0.75,
        'energy': 0.20, 'slip': 0.01,
    },
    'Water Scrubbing': {
        'min_scale': 150, 'max_scale': 5000,
        'purity_single': 0.97, 'purity_multi': 0.98,
        'cost_small': 1.00, 'cost_medium': 0.80, 'cost_large': 0.65,
        'energy': 0.30, 'slip': 0.01,
    },
    'Chemical Absorption (Amine)': {
        'min_scale': 400, 'max_scale': 10000,
        'purity_single': 0.99, 'purity_multi': 0.995,
        'cost_small': 1.60, 'cost_medium': 1.20, 'cost_large': 0.80,
        'energy': 0.45, 'slip': 0.005,
    },
    'Cryogenic': {
        'min_scale': 500, 'max_scale': 10000,
        'purity_single': 0.98, 'purity_multi': 0.99,
        'cost_small': 1.80, 'cost_medium': 1.40, 'cost_large': 1.00,
        'energy': 0.55, 'slip': 0.01,
    },
}

source_compatibility = {
    'Agriculture': {
        'Membrane': 'Recommended', 'PSA': 'Recommended',
        'Water Scrubbing': 'Highly Recommended', 'Chemical Absorption (Amine)': 'Recommended',
        'Cryogenic': 'Not Recommended',
    },
    'Sewage': {
        'Membrane': 'Possible with pre-treatment', 'PSA': 'Highly Recommended',
        'Water Scrubbing': 'Recommended', 'Chemical Absorption (Amine)': 'Recommended',
        'Cryogenic': 'Not Recommended',
    },
    'Landfill': {
        'Membrane': 'Recommended', 'PSA': 'Highly Recommended',
        'Water Scrubbing': 'Possible', 'Chemical Absorption (Amine)': 'Not Recommended',
        'Cryogenic': 'Not Recommended',
    },
    'Food Waste': {
        'Membrane': 'Possible with pre-treatment', 'PSA': 'Recommended',
        'Water Scrubbing': 'Recommended', 'Chemical Absorption (Amine)': 'Highly Recommended',
        'Cryogenic': 'Not Recommended',
    },
}

end_use_requirements = {
    'Grid Injection': {'min_purity': 0.96, 'recommended': ['PSA', 'Water Scrubbing', 'Membrane']},
    'Vehicle Fuel': {'min_purity': 0.97, 'recommended': ['PSA', 'Membrane', 'Water Scrubbing']},
    'Industrial Feedstock': {'min_purity': 0.98, 'recommended': ['Chemical Absorption (Amine)', 'Membrane']},
    'CHP': {'min_purity': 0.50, 'recommended': ['No upgrade needed']},
    'CO2 utilization': {'min_purity': 0.96, 'recommended': ['PSA', 'Water Scrubbing', 'Membrane']},
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_cost_at_scale(tech_name, scale):
    """Calculate relative cost at given plant scale (m³/h)"""
    tech = technologies[tech_name]
    if scale < 200:
        return tech['cost_small']
    elif scale < 1000:
        ratio = (scale - 200) / 800
        return tech['cost_small'] + ratio * (tech['cost_medium'] - tech['cost_small'])
    else:
        ratio = min(1.0, (scale - 1000) / 4000)
        return tech['cost_medium'] + ratio * (tech['cost_large'] - tech['cost_medium'])

def get_purity(tech_name, required_purity):
    """Get achievable purity, consider multistage for membrane if needed"""
    tech = technologies[tech_name]
    if tech_name == 'Membrane' and required_purity > 0.96:
        return tech['purity_multi']
    return tech['purity_single']

def is_suitable(tech_name, source, required_purity, scale):
    """Check if technology meets all constraints"""
    tech = technologies[tech_name]
    
    # Scale check
    if scale < tech['min_scale']:
        return False, f"Scale too small (minimum {tech['min_scale']} m³/h)"
    if scale > tech['max_scale']:
        return False, f"Scale too large (maximum {tech['max_scale']} m³/h)"
    
    # Source compatibility
    compat = source_compatibility.get(source, {}).get(tech_name, 'Not Recommended')
    if compat == 'Not Recommended':
        return False, f"Not compatible with {source} source"
    
    # Purity check
    achievable = get_purity(tech_name, required_purity)
    if achievable < required_purity:
        return False, f"Achieves only {achievable:.0%} purity, need {required_purity:.0%}"
    
    return True, compat

# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    print("\n" + "=" * 60)
    print("BIOGAS UPGRADING TECHNOLOGY SELECTOR")
    print("=" * 60)
    print("\nThis tool recommends biogas upgrading technologies based on")
    print("your plant parameters. Costs are relative and normalized.\n")
    
    # Get user inputs
    print("-" * 40)
    print("Please enter your plant parameters:")
    print("-" * 40)
    
    while True:
        try:
            scale = float(input("Plant scale (m³/h of raw biogas) [50-5000]: "))
            if 50 <= scale <= 5000:
                break
            else:
                print("Please enter a value between 50 and 5000")
        except ValueError:
            print("Please enter a valid number")
    
    print("\nAvailable feedstock sources:")
    sources = list(source_compatibility.keys())
    for i, s in enumerate(sources, 1):
        print(f"  {i}. {s}")
    while True:
        try:
            source_choice = int(input("Select feedstock (1-4): "))
            if 1 <= source_choice <= 4:
                source = sources[source_choice - 1]
                break
            else:
                print("Please enter 1, 2, 3, or 4")
        except ValueError:
            print("Please enter a number")
    
    print("\nAvailable end uses:")
    end_uses = list(end_use_requirements.keys())
    for i, e in enumerate(end_uses, 1):
        req = end_use_requirements[e]['min_purity']
        print(f"  {i}. {e} (min {req:.0%} CH₄)")
    while True:
        try:
            end_use_choice = int(input("Select end use (1-5): "))
            if 1 <= end_use_choice <= 5:
                end_use = end_uses[end_use_choice - 1]
                required_purity = end_use_requirements[end_use]['min_purity']
                break
            else:
                print("Please enter 1, 2, 3, 4, or 5")
        except ValueError:
            print("Please enter a number")
    
    # Calculate results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"\nYour parameters: {scale} m³/h | Source: {source} | End use: {end_use}")
    print(f"Required CH₄ purity: {required_purity:.0%}\n")
    
    results = []
    for tech_name in technologies.keys():
        suitable, reason = is_suitable(tech_name, source, required_purity, scale)
        cost = get_cost_at_scale(tech_name, scale)
        purity = get_purity(tech_name, required_purity)
        tech = technologies[tech_name]
        
        results.append({
            'name': tech_name,
            'suitable': suitable,
            'cost': cost,
            'purity': purity,
            'energy': tech['energy'],
            'slip': tech['slip'],
            'reason': reason
        })
    
    # Sort by cost (cheapest first)
    results.sort(key=lambda x: x['cost'] if x['suitable'] else 999)
    
    # Display suitable technologies
    suitable_techs = [r for r in results if r['suitable']]
    if suitable_techs:
        print("-" * 40)
        print("RECOMMENDED TECHNOLOGIES (sorted by cost):")
        print("-" * 40)
        for i, r in enumerate(suitable_techs, 1):
            print(f"\n{i}. {r['name']}")
            print(f"   Relative cost: {r['cost']:.2f} (normalized)")
            print(f"   Achievable purity: {r['purity']:.0%}")
            print(f"   Energy consumption: {r['energy']} kWh/m³")
            print(f"   Methane slip: {r['slip']:.1%}")
    else:
        print("\n❌ No technology matches all constraints.")
        print("Consider increasing your plant scale or choosing a different end use.\n")
    
    # Display all technologies comparison
    print("\n" + "-" * 40)
    print("FULL COMPARISON TABLE:")
    print("-" * 40)
    print(f"\n{'Technology':<28} {'Suitable':<10} {'Cost':<8} {'Purity':<8} {'Energy':<10}")
    print("-" * 65)
    for r in results:
        suitable_mark = "✓" if r['suitable'] else "✗"
        print(f"{r['name']:<28} {suitable_mark:<10} {r['cost']:<8.2f} {r['purity']:.0%}       {r['energy']} kWh/m³")
    
    print("\n" + "=" * 60)
    print("Note: Cost is relative (1.0 = baseline reference).")
    print("Actual costs depend on local electricity prices, labor, and site conditions.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()