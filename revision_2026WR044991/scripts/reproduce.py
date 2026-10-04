"""Verify archived inputs, redraw five figures, and check regenerated statistics."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import platform
import numpy as np
import pandas as pd
import matplotlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generated'


def read(path):
    return pd.read_csv(path, float_precision='round_trip')


def main():
    manifest = json.loads((ROOT / 'provenance.json').read_text(encoding='utf-8'))
    for item in manifest['input_files']:
        path = ROOT / item['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], path

    summary = read(ROOT / 'data/external/reconstruction_summary.csv')
    labelmap = read(ROOT / 'data/external/feature_labels.csv')
    OUT.mkdir(exist_ok=True)
    assert not summary.duplicated(['dataset', 'feature', 'method', 'variant']).any()
    external_report = {}
    for ds, feature_n, target_n in [('GSIM', 18, 831), ('GSCD', 17, 355), ('GSHA', 14, 803)]:
        base = ROOT / f'data/external/{ds}'
        sep = read(base / 'panels_ab_separation.csv')
        values = read(base / 'panel_c_four_line_values.csv')
        assert sep.feature.nunique() == feature_n and len(sep) == feature_n * 6
        assert len(values) == feature_n * 4
        np.testing.assert_allclose(sep.continuous_fcm_value - sep.comparator_value,
                                   sep.delta_continuous_minus_comparator, atol=1e-12)
        expected_n = lambda feature: 213 if ds == 'GSCD' and feature == 'T50' else target_n
        assert all(row.n == expected_n(row.feature) for row in sep.itertuples())
        lookup = summary[summary.dataset == ds].set_index(['feature', 'method', 'variant'])
        table_number = {'GSIM': 6, 'GSCD': 7, 'GSHA': 8}[ds]
        table = pd.read_csv(base / f'TableS{table_number}_reference.csv', dtype=str)
        labels = labelmap[labelmap.dataset == ds].set_index('label').source_feature.to_dict()
        table_methods = {'Köppen': ('Koppen', 'ClassMean'), 'Knoben': ('Knoben', 'ClassMean'),
                         'KnobenK5': ('Knoben', 'MatchedK5'), 'AUDIOS': ('Continuous_FCM', 'ClassMean'),
                         'AUDIOSK5': ('Continuous_FCM', 'MatchedK5')}
        assert len(table) == feature_n and table.Signature.is_unique
        computed_rows = []
        for _, row in table.iterrows():
            feature = labels[row.Signature]
            computed = {'Signature': row.Signature, 'Unit': row.Unit}
            for display, (method, variant) in table_methods.items():
                value = float(lookup.loc[(feature, method, variant), 'pooled_rmse'])
                text = row[display]
                digits = len(text.split('.')[1]) if '.' in text else 0
                assert abs(value - float(text)) <= 0.5 * 10 ** (-digits) + 1e-12, (ds, feature, display)
                computed[display] = value
            computed_rows.append(computed)
        pd.DataFrame(computed_rows).to_csv(OUT / f'TableS{table_number}_unrounded.csv', index=False)
        for row in values.itertuples():
            a = lookup.loc[(row.feature, 'Continuous_FCM', row.audios_variant)]
            b = lookup.loc[(row.feature, row.baseline, row.baseline_variant)]
            assert row.n == a.target_n == b.target_n == expected_n(row.feature)
            np.testing.assert_allclose([row.audios_pooled_rmse, row.baseline_pooled_rmse],
                                       [a.pooled_rmse, b.pooled_rmse], rtol=1e-12)
        np.testing.assert_allclose(values.relative_rmse_improvement_percent,
                                   100 * (values.baseline_pooled_rmse - values.audios_pooled_rmse) / values.baseline_pooled_rmse,
                                   rtol=1e-11, atol=1e-12)
        reference = read(base / 'panel_c_summary.csv')
        result = values.groupby('label', sort=False).agg(
            n_features=('feature', 'size'),
            audios_better_n=('relative_rmse_improvement_percent', lambda x: int((x > 0).sum())),
            median_improvement_percent=('relative_rmse_improvement_percent', 'median')).reset_index()
        pd.testing.assert_frame_equal(result, reference, check_exact=False, rtol=1e-11, atol=1e-12)
        external_report[ds] = dict(features=feature_n, plotted_comparisons=len(values), table_cells_verified=feature_n * 5,
                                   targets=target_n, T50_targets=expected_n('T50'))

    for args in [['plot_figure8.py'], ['plot_external_si.py', 'GSCD'],
                 ['plot_external_si.py', 'GSHA'], ['plot_daily.py']]:
        subprocess.run([sys.executable, str(ROOT / 'scripts' / args[0]), *args[1:]], check=True)

    daily_report = {}
    for name in ['Figure9', 'FigureS17']:
        base = ROOT / f'data/daily/{name}'
        for file in ['boxplot_statistics.csv', 'plotted_statistics.csv', 'histogram_bins.csv']:
            actual = read(OUT / name / file)
            expected = read(base / file)
            pd.testing.assert_frame_equal(actual, expected, check_exact=False, rtol=1e-10, atol=1e-10)
        # Verify the plotted score sets, not only summary statistics.
        for file in ['boxplot_source_values.csv', 'paired_source_values.csv']:
            expected = read(base / file)
            actual = read(OUT / name / file)
            keys = ['window', 'method', 'basin_id', 'plotted_metric']
            assert not actual.duplicated(keys).any()
            pd.testing.assert_frame_equal(actual.sort_values(keys).reset_index(drop=True),
                                          expected.sort_values(keys).reset_index(drop=True),
                                          check_exact=False, rtol=1e-12, atol=1e-12)
        daily_report[name] = read(OUT / name / 'plotted_statistics.csv').to_dict(orient='records')
        checks = json.loads((OUT / name / 'checks.json').read_text())
        assert checks['boxplot_common_n'] == 626 and checks['paired_common_n'] == 627
        assert checks['equal_displayed_bin_widths'] and checks['zero_is_bin_edge']
        assert checks['median_lines_at_true_positions']

    report = dict(status='PASS', input_files_verified=len(manifest['input_files']),
                  scope='Replotting and summary checks from supplied intermediate results; no model rerun',
                  external=external_report, daily=daily_report,
                  environment=dict(python=platform.python_version(), numpy=np.__version__,
                                   pandas=pd.__version__, matplotlib=matplotlib.__version__))
    (OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('PASS: five figures regenerated; input hashes, external comparisons, daily scores and statistics verified.')


if __name__ == '__main__':
    main()
