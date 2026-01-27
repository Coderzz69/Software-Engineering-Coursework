"""
Tariff Service Module
---------------------
Calculates electricity bills based on Lab Task specifications.

Module: tariff_service.py
Purpose: Calculate bills using tiered slab rates with minimum charge
Input: Units consumed (float)
Output: Bill amount and detailed breakdown
Author: Software Engineering Lab
Date: 2026-01-27

Lab Task 1 Specification:
--------------------------
Rate per unit:
1. First 50 units: ₹1.5
2. Next 50 units (51-100): ₹2.5
3. Next 50 units (101-150): ₹3.5
4. Above 150 units: ₹4.5

Minimum charge: ₹25 when units = 0
"""

from decimal import Decimal
from typing import Dict, List
from modules.constants import TARIFF_SLABS, MINIMUM_CHARGE


class TariffService:
    @staticmethod
    def calculate_bill(units: float) -> Dict:
        """
        Calculate electricity bill based on lab-specified tiered slab rates.
        
        Preconditions:
        - units is a non-negative number
        
        Logic:
        1. Check if units == 0, apply minimum charge
        2. For each slab, calculate units consumed in that slab
        3. Multiply slab units by slab rate
        4. Accumulate total and create breakdown
        5. Return total amount with detailed breakdown
        
        Algorithm:
        ----------
        IF units == 0:
            RETURN minimum_charge (₹25)
        ELSE:
            total = 0
            remaining = units
            breakdown = []
            
            FOR each (slab_limit, rate) in TARIFF_SLABS:
                IF remaining <= 0:
                    BREAK
                slab_units = MIN(remaining, slab_limit)
                amount = slab_units * rate
                total = total + amount
                breakdown.append({slab, units, rate, amount})
                remaining = remaining - slab_units
            
            RETURN {total, breakdown, minimum_charge_applied}
        
        Input:
        - units (float): Number of units consumed
        
        Output:
        - dict: {
            'base_amount': float - Total calculated amount
            'minimum_charge_applied': bool - Whether minimum charge was applied
            'breakdown': list - Slab-wise breakdown
          }
        
        Examples:
        >>> TariffService.calculate_bill(0)
        {'base_amount': 25.0, 'minimum_charge_applied': True, 'breakdown': []}
        
        >>> TariffService.calculate_bill(50)
        {'base_amount': 75.0, 'minimum_charge_applied': False, 
         'breakdown': [{'slab': '0-50', 'units': 50, 'rate': 1.5, 'amount': 75.0}]}
        
        >>> TariffService.calculate_bill(150)
        {'base_amount': 375.0, 'minimum_charge_applied': False,
         'breakdown': [...]}  # 50*1.5 + 50*2.5 + 50*3.5 = 375
        """
        units = Decimal(str(units))
        
        # Special case: Zero units consumed
        if units == 0:
            return {
                'base_amount': float(MINIMUM_CHARGE),
                'minimum_charge_applied': True,
                'breakdown': []
            }
        
        total = Decimal('0.00')
        remaining_units = units
        breakdown = []
        slab_start = 0
        
        # Calculate for each slab
        for slab_limit, rate in TARIFF_SLABS:
            if remaining_units <= 0:
                break
            
            # Calculate units in this slab
            slab_units = min(remaining_units, Decimal(str(slab_limit)))
            slab_rate = Decimal(str(rate))
            slab_amount = slab_units * slab_rate
            
            # Add to total
            total += slab_amount
            
            # Create slab label
            if slab_limit == float('inf'):
                slab_label = f"{slab_start+1}+"
            else:
                slab_end = slab_start + int(slab_limit)
                slab_label = f"{slab_start+1}-{slab_end}"
            
            # Add to breakdown
            breakdown.append({
                'slab': slab_label,
                'units': float(slab_units),
                'rate': float(slab_rate),
                'amount': float(slab_amount)
            })
            
            # Update remaining and slab start
            remaining_units -= slab_units
            if slab_limit != float('inf'):
                slab_start += int(slab_limit)
        
        return {
            'base_amount': float(total.quantize(Decimal('0.01'))),
            'minimum_charge_applied': False,
            'breakdown': breakdown
        }
