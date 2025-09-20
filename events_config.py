# events_config.py — student-friendly wording + rich feedback (safe quoting)

EVENTS = {
    "2": {
        "id": "w2_supplier_delay_tops",
        "title": "Week 2 — Some t-shirts will arrive late (Tops)",
        "description": (
            "Your main t-shirt supplier tells you a batch will arrive about a week late. "
            "That could leave shelves thin for popular Tops this month. Choose how to reduce the risk of stockouts."
        ),
        "choices": [
            {
                "id": "A",
                "label": "Pay extra shipping to rush a portion in now.",
                "transform": "w2_A_expedite_40",
                "student_feedback": [
                    """WHAT YOU DID: You paid for faster shipping so part of the delayed t-shirts arrive sooner.""",
                    """GOOD OUTCOMES: Fewer empty shelves in Tops; more sales captured while demand is hot.""",
                    """TRADE-OFFS / RISKS: Higher costs this month; gross margin % will dip a bit.""",
                    """WHAT TO LOOK FOR IN CHARTS: Pie (latest month) — Tops slice a little larger; Compact — Quantity lines nudge up; KPIs — Revenue up slightly, GM% down slightly.""",
                    """WHAT TO WATCH NEXT WEEK: If demand stays strong, consider if the cost of expediting keeps paying off.""",
                ],
                "instructor_note": "Discuss service level vs. cost. When does paying to protect availability make sense?",
            },
            {
                "id": "B",
                "label": "Don't rush; instead, discount other categories to shift demand.",
                "transform": "w2_B_shift_demand_markdown",
                "student_feedback": [
                    """WHAT YOU DID: You used small discounts elsewhere to steer shoppers to other items while you wait.""",
                    """GOOD OUTCOMES: Cash is preserved (no rush fees) and other categories move faster.""",
                    """TRADE-OFFS / RISKS: Discounts lower margin; you may not fully replace lost Tops sales.""",
                    """WHAT TO LOOK FOR IN CHARTS: Pie — Other items’ slices grow, Tops shrink a bit; Compact — Revenue mix shifts; KPIs — GM% softens due to markdowns.""",
                    """WHAT TO WATCH NEXT WEEK: If Tops keep running short, compare the margin hit of markdowns vs. expediting.""",
                ],
                "instructor_note": "Demand shaping via price and the limits of substitution.",
            },
            {
                "id": "C",
                "label": "Buy a smaller amount from a backup supplier.",
                "transform": "w2_C_partial_substitute",
                "student_feedback": [
                    """WHAT YOU DID: You sourced about a quarter of the delayed t-shirts from another vendor.""",
                    """GOOD OUTCOMES: Better shelf availability than waiting; some sales protected.""",
                    """TRADE-OFFS / RISKS: Higher cost per unit and possible quality differences (returns risk).""",
                    """WHAT TO LOOK FOR IN CHARTS: Pie — Tops slice stabilizes; KPIs — COGS tick up, Profit may be flat to slightly down.""",
                    """WHAT TO WATCH NEXT WEEK: Keep an eye on returns or reviews for those substitute units.""",
                ],
                "instructor_note": "Vendor diversification and quality risk management.",
            },
        ],
    },

    "3": {
        "id": "w3_heat_wave_shorts",
        "title": "Week 3 — Heat wave → shorts selling faster (Bottoms)",
        "description": (
            "Warmer-than-usual weather is pushing up demand for shorts for about two weeks. "
            "Decide how to make the most of this bump without running out."
        ),
        "choices": [
            {
                "id": "A",
                "label": "Boost online ads for shorts to catch extra demand.",
                "transform": "w3_A_boost_demand_ads",
                "student_feedback": [
                    """WHAT YOU DID: You increased marketing for shorts while demand is naturally higher.""",
                    """GOOD OUTCOMES: More shoppers find shorts; you sell more units while the spike lasts.""",
                    """TRADE-OFFS / RISKS: Marketing spend rises; if stock runs tight, ads can waste spend.""",
                    """WHAT TO LOOK FOR IN CHARTS: Pie — Bottoms slice gets bigger; Compact — Quantity up, Marketing $ up; KPIs — Revenue up, Profit up if margin holds.""",
                    """WHAT TO WATCH NEXT WEEK: Watch inventory for stockout risk; consider moving stock between stores.""",
                ],
                "instructor_note": "Right-time promotion vs. stock availability; ROAS thinking.",
            },
            {
                "id": "B",
                "label": "Limit shorts to 3 per customer to spread stock.",
                "transform": "w3_B_limit_per_customer",
                "student_feedback": [
                    """WHAT YOU DID: You set a fair-purchase limit so more shoppers can find shorts.""",
                    """GOOD OUTCOMES: Fewer stockouts; steadier on-shelf presence.""",
                    """TRADE-OFFS / RISKS: Slightly fewer total units sold; some customers might dislike limits.""",
                    """WHAT TO LOOK FOR IN CHARTS: Compact — Quantity dips a little vs. ads; Inventory holds up better; KPIs — Profit steady to slightly lower.""",
                    """WHAT TO WATCH NEXT WEEK: Check sentiment; if supply improves, remove limits quickly.""",
                ],
                "instructor_note": "Customer equity vs. pure revenue maximization.",
            },
            {
                "id": "C",
                "label": "Shift extra shorts from slow stores to hot stores.",
                "transform": "w3_C_crossdock",
                "student_feedback": [
                    """WHAT YOU DID: You moved inventory from where it’s not selling to where it is.""",
                    """GOOD OUTCOMES: Better match of stock to demand; more sales where needed.""",
                    """TRADE-OFFS / RISKS: Small transfer cost and coordination work.""",
                    """WHAT TO LOOK FOR IN CHARTS: Compact — Quantity up; Inventory down in hot areas; KPIs — Profit up slightly; COGS & costs up just a touch.""",
                    """WHAT TO WATCH NEXT WEEK: If heat persists, keep transfers going; if not, stop to avoid over-handling.""",
                ],
                "instructor_note": "Network rebalancing under local demand spikes.",
            },
        ],
    },

    "4": {
        "id": "w4_linen_returns",
        "title": "Week 4 — A batch of linen shirts is getting returned (Tops subset)",
        "description": (
            "Shoppers report stitching problems on a specific batch of linen shirts. "
            "You need to protect the brand and avoid throwing away margin."
        ),
        "choices": [
            {
                "id": "A",
                "label": "Pull the batch, fix quality, and re-release slowly.",
                "transform": "w4_A_rework_quality",
                "student_feedback": [
                    """WHAT YOU DID: You took the affected shirts off the floor to repair them before selling again.""",
                    """GOOD OUTCOMES: Protects brand trust; future returns drop.""",
                    """TRADE-OFFS / RISKS: Extra labor cost now; slower revenue this week.""",
                    """WHAT TO LOOK FOR IN CHARTS: Compact — Inventory dips a bit, Profit soft; KPIs — GM% stable (no heavy discounting).""",
                    """WHAT TO WATCH NEXT WEEK: Confirm return rates normalize; watch customer reviews rebound.""",
                ],
                "instructor_note": "Short-term pain to avoid long-term reputation damage.",
            },
            {
                "id": "B",
                "label": "Put that batch on deep discount and clear it fast.",
                "transform": "w4_B_clearance",
                "student_feedback": [
                    """WHAT YOU DID: You discounted heavily to sell through quickly and move on.""",
                    """GOOD OUTCOMES: Clears the issue and frees up space; fewer complaints later.""",
                    """TRADE-OFFS / RISKS: Big margin hit on those units.""",
                    """WHAT TO LOOK FOR IN CHARTS: Pie — Tops may grow in units; KPIs — Revenue may rise but GM% drops; Compact — Quantity up, Profit down.""",
                    """WHAT TO WATCH NEXT WEEK: Replace that space with reliable items; make sure staff can explain the markdown story.""",
                ],
                "instructor_note": "Cash recovery and speed vs. gross margin.",
            },
            {
                "id": "C",
                "label": "Ask the supplier for a credit; pause reorders for now.",
                "transform": "w4_C_credit_pause",
                "student_feedback": [
                    """WHAT YOU DID: You recovered part of your cost via supplier credit and held off future buys.""",
                    """GOOD OUTCOMES: Better cash position; motivates supplier to fix the issue.""",
                    """TRADE-OFFS / RISKS: Fewer shirts on hand; possible short-term gaps in Tops choices.""",
                    """WHAT TO LOOK FOR IN CHARTS: KPIs — COGS down a bit, inventory down; Compact — Quantity may dip; Profit could hold if credit offsets.""",
                    """WHAT TO WATCH NEXT WEEK: Monitor availability; re-open POs once quality is confirmed.""",
                ],
                "instructor_note": "Vendor accountability and cash protection.",
            },
        ],
    },

    "5": {
        "id": "w5_cotton_cost_spike",
        "title": "Week 5 — Cotton costs jump for incoming items",
        "description": (
            "A rise in cotton prices means some incoming Tops and Bottoms will cost more to buy. "
            "Choose how to protect margin without scaring off customers."
        ),
        "choices": [
            {
                "id": "A",
                "label": "Hedge about half your exposure (pay a small fee to stabilize cost).",
                "transform": "w5_A_hedge",
                "student_feedback": [
                    """WHAT YOU DID: You paid a fee to smooth out cost increases for about half of affected items.""",
                    """GOOD OUTCOMES: More predictable costs; fewer surprises to margin.""",
                    """TRADE-OFFS / RISKS: The fee slightly reduces profit even if costs fall later.""",
                    """WHAT TO LOOK FOR IN CHARTS: KPIs — COGS up modestly vs. full spike; Profit steadier than no hedge; Compact — Profit line less bumpy.""",
                    """WHAT TO WATCH NEXT WEEK: Re-check the fee vs. benefit if cotton prices move again.""",
                ],
                "instructor_note": "Risk reduction vs. carrying the fee.",
            },
            {
                "id": "B",
                "label": "Raise prices a little (protect margin, keep key value items flat).",
                "transform": "w5_B_price_up",
                "student_feedback": [
                    """WHAT YOU DID: You raised prices a bit on most affected items, but kept key price points unchanged.""",
                    """GOOD OUTCOMES: Margin dollars protected on many items; revenue can hold up.""",
                    """TRADE-OFFS / RISKS: Some shoppers buy slightly less; units dip a little.""",
                    """WHAT TO LOOK FOR IN CHARTS: KPIs — Sales Revenue OK, Profit OK; Compact — Quantity edges down; GM$ stable or up slightly.""",
                    """WHAT TO WATCH NEXT WEEK: Watch demand for pushback; roll back if sensitivity is higher than expected.""",
                ],
                "instructor_note": "Price elasticity and key-value item strategy.",
            },
            {
                "id": "C",
                "label": "Use more blended fabrics in place of pure cotton for some items.",
                "transform": "w5_C_blend_substitute",
                "student_feedback": [
                    """WHAT YOU DID: You switched part of the assortment to blends to lower cost pressure.""",
                    """GOOD OUTCOMES: Costs rise less than a full cotton spike; margin pressure softens.""",
                    """TRADE-OFFS / RISKS: Slight quality-perception risk; possible small increase in returns.""",
                    """WHAT TO LOOK FOR IN CHARTS: KPIs — COGS up only a little; Profit steadier; Compact — Quantity nearly flat; Pie — minor mix changes.""",
                    """WHAT TO WATCH NEXT WEEK: Monitor reviews and returns; adjust blends if customers push back.""",
                ],
                "instructor_note": "Cost/quality/brand balance and customer perception.",
            },
        ],
    },

    "6": {
        "id": "w6_dc_labor_shortage",
        "title": "Week 6 — Warehouse short-staffed → slower shipping out to stores",
        "description": (
            "Your distribution center is short on labor, slowing shipments to stores. "
            "Decide how to protect shelf availability and sales service levels."
        ),
        "choices": [
            {
                "id": "A",
                "label": "Hire temporary help for about 6 weeks.",
                "transform": "w6_A_temp_staff",
                "student_feedback": [
                    """WHAT YOU DID: You added temporary staff to speed up outbound work.""",
                    """GOOD OUTCOMES: Better on-time deliveries; fewer stockouts in stores.""",
                    """TRADE-OFFS / RISKS: Higher operating cost this month.""",
                    """WHAT TO LOOK FOR IN CHARTS: Compact — Quantity improves; KPIs — Marketing/OpEx proxy up a bit, Profit should still benefit if sales lift beats added cost.""",
                    """WHAT TO WATCH NEXT WEEK: If volume normalizes, scale temp help down quickly.""",
                ],
                "instructor_note": "Paying for service recovery vs. near-term OpEx.",
            },
            {
                "id": "B",
                "label": "Prioritize your top-selling items; slower items wait.",
                "transform": "w6_B_prioritize_top",
                "student_feedback": [
                    """WHAT YOU DID: You focused limited capacity on your most popular items.""",
                    """GOOD OUTCOMES: Best sellers stay in stock; top-line impact is protected.""",
                    """TRADE-OFFS / RISKS: Long-tail items may be under-served; fairness across stores can suffer.""",
                    """WHAT TO LOOK FOR IN CHARTS: Compact — Quantity holds or grows on top items; KPIs — Profit stable; some items’ inventory may rise (waiting).""",
                    """WHAT TO WATCH NEXT WEEK: Rotate priorities if star items change to avoid long-tail frustration.""",
                ],
                "instructor_note": "Allocation under constraint and equity across the network.",
            },
            {
                "id": "C",
                "label": "Let suppliers ship a small set directly to customers (drop-ship).",
                "transform": "w6_C_dropship",
                "student_feedback": [
                    """WHAT YOU DID: You let suppliers ship certain items directly to customers.""",
                    """GOOD OUTCOMES: Takes load off your warehouse; faster for those items.""",
                    """TRADE-OFFS / RISKS: Per-unit shipping cost a bit higher; customer experience can vary by supplier.""",
                    """WHAT TO LOOK FOR IN CHARTS: KPIs — COGS/Costs inch up; Quantity modestly up; Compact — Profit up slightly if extra sales beat the cost.""",
                    """WHAT TO WATCH NEXT WEEK: Track delivery times and customer feedback per supplier.""",
                ],
                "instructor_note": "Channel strategy: speed vs. cost and CX control.",
            },
        ],
    },

    "7": {
        "id": "w7_competitor_omni_promo",
        "title": "Week 7 — A competitor launches a big sale across similar items",
        "description": (
            "A competitor is running a broad promotion that overlaps with your Tops/Bottoms/Accessories. "
            "Choose how to defend your customers and margin."
        ),
        "choices": [
            {
                "id": "A",
                "label": "Run selective discounts + extra loyalty points on key items.",
                "transform": "w7_A_counter_promo",
                "student_feedback": [
                    """WHAT YOU DID: You matched in a focused way on a few items and rewarded loyal customers.""",
                    """GOOD OUTCOMES: Keeps shoppers from switching; unit sales rise on targeted SKUs.""",
                    """TRADE-OFFS / RISKS: Margin % gets slimmer on those SKUs; watch discount creep.""",
                    """WHAT TO LOOK FOR IN CHARTS: Pie — Targeted categories gain share; KPIs — Revenue up, GM% down a bit; Compact — Quantity up, Profit depends on discount depth.""",
                    """WHAT TO WATCH NEXT WEEK: Turn off promos quickly where they’re not needed; check loyalty repeat rate.""",
                ],
                "instructor_note": "Defensive pricing, loyalty lift, and promo discipline.",
            },
            {
                "id": "B",
                "label": "Stand out with a small premium collection; cut weak sellers.",
                "transform": "w7_B_differentiate",
                "student_feedback": [
                    """WHAT YOU DID: You leaned into premium choices and trimmed slow SKUs to focus your offer.""",
                    """GOOD OUTCOMES: Stronger brand feel; higher average price can support profit dollars.""",
                    """TRADE-OFFS / RISKS: Fewer total units sold in the short term; needs good storytelling.""",
                    """WHAT TO LOOK FOR IN CHARTS: KPIs — Unit price up, GM$ stable or better; Compact — Revenue may hold with fewer units; Pie — mix shifts to categories like Outerwear/Shoes/Dresses.""",
                    """WHAT TO WATCH NEXT WEEK: Watch reviews and sell-through; refresh the tail again if needed.""",
                ],
                "instructor_note": "Assortment curation and value perception.",
            },
            {
                "id": "C",
                "label": "Focus on the experience (events, staff styling, micro-influencers).",
                "transform": "w7_C_experience_led",
                "student_feedback": [
                    """WHAT YOU DID: You invested in events and social buzz instead of heavy discounts.""",
                    """GOOD OUTCOMES: More traffic and engagement; less pressure on prices.""",
                    """TRADE-OFFS / RISKS: Marketing spend and benefits may take 2–3 weeks to fully show up.""",
                    """WHAT TO LOOK FOR IN CHARTS: KPIs — Marketing $ up; Quantity up modestly; Compact — Profit grows gradually if traffic converts.""",
                    """WHAT TO WATCH NEXT WEEK: Track conversion and basket size; stay consistent so momentum builds.""",
                ],
                "instructor_note": "Brand-building vs. immediate promo payback.",
            },
        ],
    },
}
