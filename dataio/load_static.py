import pandas as pd
from stemp_abw.models import FeedinTs, DemandTs, MunData, RepoweringScenario


def load_timeseries():
    """Load and format time series for all municipalities XXX

    Notes
    -----
    * renewable timeseries from DB are normalized
    * demand timeseries from DB are absolute in MW
    """

    timeseries = {}

    # load normalized feedin ts
    ts_feedin = pd.DataFrame(list(
        FeedinTs.objects \
            .order_by('timestamp') \
            .values_list('ags_id', 'wind_sq', 'wind_fs',
                         'pv_ground', 'pv_roof',
                         'hydro', 'bio', 'conventional', named=True)))
    # create normalized feedin DF with technology & mun MultiIndex on columns
    timeseries['feedin'] = ts_feedin \
        .pivot(index=ts_feedin.index, columns='ags_id') \
        .apply(lambda _: pd.Series(_.dropna().values)) \
        .fillna(0)

    # load demand ts
    ts_demand = pd.DataFrame(list(
        DemandTs.objects \
            .order_by('timestamp') \
            .values_list('ags_id', 'el_ind', 'el_rca',
                         'el_hh', named=True)))
    # create feedin DF with demand type & mun MultiIndex on columns
    timeseries['demand'] = ts_demand \
        .pivot(index=ts_demand.index, columns='ags_id') \
        .apply(lambda _: pd.Series(_.dropna().values)) \
        .fillna(0)

    return timeseries


def load_mun_data():
    """Load municipality statistics"""

    mun_data = pd.DataFrame(list(
        MunData.objects \
            .order_by('ags_id') \
            .values())).set_index('ags_id')

    return mun_data


def load_repowering_scenarios():
    """Load repowering scenarios"""
    return RepoweringScenario.objects.order_by('id').all()
