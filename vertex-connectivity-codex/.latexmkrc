# Run latexmk from this project root to compile the current editable drafts.
# Explicit targets exclude archived snapshots under results/.
@default_files = (
    'manuscript/lower_bound_candidate.tex',
    'sources/prior-notes/vertex_connectivity_research_note.tex',
    'sources/prior-notes/deterministic_connectivity_lower_bounds.tex',
);

$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 %O %S';

# Keep generated PDFs and auxiliary files out of the source directories.
$out_dir = 'build';
$aux_dir = $out_dir;
