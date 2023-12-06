# pylint: disable=invalid-name


"""Semiconductor ALD SSAProbSolver."""


from openssa.contrib import StreamlitSSAProbSolver


StreamlitSSAProbSolver(unique_name='PROBLEM-SOLVING SSA',
                       domain='Atomic Layer Deposition (ALD) for Semiconductor',
                       prob=('Estimate the ALD process time for 10 cycles, '
                             'each with Pulse Time = 15 secs, Purge Time = 10 secs and negligible Inert'),
                       expert_heuristics=('Purge Time must be at least as long as Pulse Time in each cycle '
                                          'to ensure all excess precursor and reaction byproducts are removed '
                                          'from the chamber before the next cycle begins'),
                       doc_src_path='s3://aitomatic-public/KnowledgeBase/Semiconductor/ALD')
