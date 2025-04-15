-- Solution for intermediate challenge #5 on joining multiple tables for evolution chains
SELECT
    ec.evolution_chain_id AS chain_id,
    basic.name AS basic_form,
    em1.method_name AS basic_to_middle_method,
    ec.evolution_requirement,
    middle.name AS middle_form,
    em2.method_name AS middle_to_final_method,
    ec.evolution_requirement2,
    final.name AS final_form
FROM
    evolution_chains ec
    JOIN pokemon_species basic ON ec.basic_form_id = basic.species_id
    JOIN pokemon_species middle ON ec.middle_form_id = middle.species_id
    JOIN pokemon_species final ON ec.final_form_id = final.species_id
    JOIN evolution_methods em1 ON ec.basic_to_middle_method = em1.method_id
    JOIN evolution_methods em2 ON ec.middle_to_final_method = em2.method_id
WHERE
    ec.middle_form_id IS NOT NULL
    AND ec.final_form_id IS NOT NULL
ORDER BY
    chain_id;
