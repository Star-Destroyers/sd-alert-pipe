# Star Destroyers Alert Pipeline
Star Destroyer library for interfacing with various brokers.

Currently supported brokers:

* [Lasair](sd_alert_pipe/lasair.py)
* [Alerce](sd_alert_pipe/alerce.py)
* [Antares](sd_alert_pipe/antares.py)

Each of the above modules defines a service which contains various methods for fetching data from the respective APIs, usually for a specific ZTF name.

## Installation
In a fresh virtualenv, `pip install -r requirements.txt`

## Usage
In your scripts, import `gather_data()` from [common.py](sd_alert_pipe/common.py) which takes a single ZTF name and returns an object containing results from the various brokers:

```python
from sd_alert_pipe.common import gather_data

result = await gather_data('ZTF18aaviokz')

print(result.lasair)
print(result.lasair.classification)
print(result.alerce)
print(result.alerce.classification)
print(result.antares)
```

This module takes advantage of Python3 coroutines due to the amount of network calls being made. **You'll need Python 3.8 or newer** to run this code. Using asynchronous HTTP requests speeds up fetching data by \~n, where n is the number of HTTP requests being made.

## Cli Tool

There is a simple command line tool at [cli.py](cli.py). You can use it to check the results of a Lasair stored query, or dump the contents of a call to `gather_data()`:

    $ python cli.py lasair-query 2TDE-candidates-EA
    Name          UTC                  Rising       Fading       Age       Class.
    ZTF18aaviokz  2021-03-01 11:40:05                            0.08264   NT
    ZTF18aaviokz  2021-03-01 09:56:06                            0.01043   NT
    ZTF21aaiahsu  2021-02-24 19:53:58  rising/peak


Or to use `gather_data()` from the command line:

    $ python cli.py fetch-object ZTF18aaviokz
    {
      "name": "ZTF18aaviokz",
      "lasair": {
        "name": "ZTF18aaviokz",
        "broker_id": "ZTF18aaviokz",
        "url": "https://lasair-iris.roe.ac.uk/object/ZTF18aaviokz",
        "ra": 207.86824529,
        "dec": 40.44790662,
        "classification": {
          "classifications": {
            "ZTF18aaviokz": [
              "NT",
              "The transient is synonymous with <em><a href=\"http://skyserver.sdss.org/dr12/en/tools/explore/Summary.aspx?id=1237662195070926980\">SDSS J135128.3+402652.3</a></em>; a V=15.99 mag galaxy found in the SDSS/GSC/2MASS/GAIA/GLADE catalogues. It's located 0.2\" (0.4 Kpc) from the galaxy core. A host z=0.096 implies a <em>m - M =</em> 38.23."
            ]
          },
          "crossmatches": [
            {
              "transient_object_id": "ZTF18aaviokz",
              "association_type": "NT",
              "catalogue_table_name": "SDSS/GSC/2MASS/GAIA/GLADE",
              "catalogue_object_id": "1237662195070926980",
              "catalogue_object_type": "galaxy",
              "raDeg": 207.868301,
              "decDeg": 40.447865,
              "separationArcsec": 0.21,
              "northSeparationArcsec": "0.2967600128",
              "eastSeparationArcsec": "0.2785585840",
              "physical_separation_kpc": 0.38,
              "direct_distance": null,
              "distance": 441.76,
              "z": 0.1,
              "photoZ": 0.08,
              "photoZErr": 0.02,
              "Mag": 16.29,
              "MagFilter": "r",
              "MagErr": 0.0,
              "classificationReliability": 1
            }
          ]
        },
        "data": {
          "objectId": "ZTF18aaviokz",
          "decmean": 40.44790662,
          "decstd": 0.15777948642309786,
          "ramean": 207.86824529,
          "rastd": 0.2598186342468685,
          "glatmean": 71.80428295535951,
          "glonmean": 83.7998871965549,
          "jdgmax": 2459274.9765046,
          "gmag": 19.1259,
          "dmdt_g": -0.0833096,
          "dmdt_g_2": 0.013044,
          "mag_g02": 19.0822,
          "mag_g08": 19.0105,
          "mag_g28": 19.3133,
          "maggmax": 19.7441,
          "maggmean": 19.0516,
          "maggmin": 18.7512,
          "jdrmax": 2459274.9035301,
          "mag_r02": 19.0261,
          "mag_r08": 19.0203,
          "mag_r28": 19.0091,
          "rmag": 19.0262,
          "dmdt_r": -0.00220012,
          "dmdt_r_2": null,
          "magrmax": 19.0262,
          "magrmean": 19.0131,
          "magrmin": 19.0,
          "jdmax": 2459274.9035301,
          "jdmin": 2459253.887037,
          "ncand": 10,
          "ncandgp": 8,
          "distpsnr1": 0.456524,
          "sgscore1": 0.105827,
          "sgmag1": 17.5926,
          "srmag1": 16.98,
          "htm16": 59271501911,
          "g_minus_r": -0.2236,
          "jd_g_minus_r": 2459263.0060417,
          "ncandgp_7": 3,
          "ncandgp_14": 6
        }
      },
      "alerce": {
        "name": "ZTF18aaviokz",
        "broker_id": "ZTF18aaviokz",
        "url": "https://alerce.online/object/ZTF18aaviokz",
        "ra": 207.868253527273,
        "dec": 40.4479136909091,
        "classification": {
          "late_classifier": {
            "oid": "ZTF18aaviokz",
            "Ceph_prob": 0.031392,
            "DSCT_prob": 0.020492,
            "EBC_prob": 0.029212,
            "EBSD/D_prob": 0.018312,
            "Periodic-Other_prob": 0.03052,
            "RRL_prob": 0.088072,
            "AGN-I_prob": 0.181016,
            "Blazar_prob": 0.021296,
            "CV/Nova_prob": 0.02178,
            "LPV_prob": 0.000968,
            "QSO-I_prob": 0.013552,
            "RS-CVn_prob": 0.003388,
            "SLSN_prob": 0.11988,
            "SNII_prob": 0.10152,
            "SNIa_prob": 0.16956,
            "SNIbc_prob": 0.14904
          },
          "early_classifier": {
            "oid": "ZTF18aaviokz",
            "agn_prob": 0.278467983007431,
            "sn_prob": 0.355701446533203,
            "vs_prob": 0.0964668020606041,
            "asteroid_prob": 0.0895882472395897,
            "classifier_version": null,
            "bogus_prob": 0.179775431752205
          }
        },
        "data": {
          "oid": "ZTF18aaviokz",
          "nobs": 11,
          "mean_magap_g": 18.9107372760773,
          "mean_magap_r": 19.3202673594157,
          "median_magap_g": 18.8183002471924,
          "median_magap_r": 19.1965007781982,
          "max_magap_g": 19.5009994506836,
          "max_magap_r": 19.736400604248,
          "min_magap_g": 18.6499004364014,
          "min_magap_r": 19.0279006958008,
          "sigma_magap_g": 0.29230517426741,
          "sigma_magap_r": 0.370110328195686,
          "last_magap_g": 18.9972991943359,
          "last_magap_r": 19.1965007781982,
          "first_magap_g": 19.5009994506836,
          "first_magap_r": 19.736400604248,
          "mean_magpsf_g": 19.0515694618225,
          "mean_magpsf_r": 19.2204755147298,
          "median_magpsf_g": 18.9139461517334,
          "median_magpsf_r": 19.0261917114258,
          "max_magpsf_g": 19.7441272735596,
          "max_magpsf_r": 19.6352672576904,
          "min_magpsf_g": 18.7511806488037,
          "min_magpsf_r": 18.9999675750732,
          "sigma_magpsf_g": 0.358055637951624,
          "sigma_magpsf_r": 0.359459411968973,
          "last_magpsf_g": 19.1258563995361,
          "last_magpsf_r": 19.0261917114258,
          "first_magpsf_g": 19.7441272735596,
          "first_magpsf_r": 19.6352672576904,
          "meanra": 207.868253527273,
          "meandec": 40.4479136909091,
          "sigmara": 7.71696454683969e-05,
          "sigmadec": 4.97075136082909e-05,
          "deltajd": 998.194710600095,
          "lastmjd": 59274.4765046001,
          "firstmjd": 58276.281794,
          "period": null,
          "catalogid": null,
          "classxmatch": null,
          "classrf": 7,
          "pclassrf": 0.181016,
          "pclassearly": 0.355701446533203,
          "classearly": 19
        }
      },
      "antares": {
        "name": "ZTF18aaviokz",
        "broker_id": "ANT2018akftg",
        "url": "http://api.antares.noirlab.edu/v1/loci?sort=-properties.newest_alert_observation_time&elasticsearch_query%5Blocus_listing%5D=%7B%22query%22%3A+%7B%22bool%22%3A+%7B%22filter%22%3A+%7B%22term%22%3A+%7B%22properties.ztf_object_id%22%3A+%22ZTF18aaviokz%22%7D%7D%7D%7D%7D",
        "ra": 207.8682535299866,
        "dec": 40.44792148002564,
        "data": {
          "data": [
            {
              "type": "locus_listing",
              "id": "ANT2018akftg",
              "meta": {
                "explanation": {
                  "value": 0.0,
                  "description": "sum of:",
                  "details": [
                    {
                      "value": 0.0,
                      "description": "match on required clause, product of:",
                      "details": [
                        {
                          "value": 0.0,
                          "description": "# clause",
                          "details": []
                        },
                        {
                          "value": 1.0,
                          "description": "properties.ztf_object_id:ZTF18aaviokz",
                          "details": []
                        }
                      ]
                    },
                    {
                      "value": 0.0,
                      "description": "match on required clause, product of:",
                      "details": [
                        {
                          "value": 0.0,
                          "description": "# clause",
                          "details": []
                        },
                        {
                          "value": 1.0,
                          "description": "-ConstantScore(DocValuesFieldExistsQuery [field=properties.replaced_by]) #*:*",
                          "details": []
                        }
                      ]
                    }
                  ]
                }
              },
              "attributes": {
                "dec": 40.44792148002564,
                "properties": {
                  "ztf_object_id": "ZTF18aaviokz",
                  "num_alerts": 64,
                  "num_mag_values": 11,
                  "newest_alert_id": "ztf_candidate:1520476502515015000",
                  "brightest_alert_id": "ztf_candidate:1510404692515015000",
                  "brightest_alert_magnitude": 18.75118064880371,
                  "brightest_alert_observation_time": 59264.40469910018,
                  "newest_alert_magnitude": 19.125856399536133,
                  "newest_alert_observation_time": 59274.47650460014,
                  "oldest_alert_id": "ztf_candidate:522281792515010000",
                  "oldest_alert_magnitude": 19.63526725769043,
                  "oldest_alert_observation_time": 58276.28179399995,
                  "ztf_ssnamenr": "null",
                  "feature_amplitude_magn_g": 0.4964733123779297,
                  "feature_anderson_darling_normal_magn_g": 0.75151798847213,
                  "feature_beyond_1_std_magn_g": 0.14285714285714285,
                  "feature_beyond_2_std_magn_g": 0.0,
                  "feature_cusum_magn_g": 0.39294228299933803,
                  "feature_eta_e_magn_g": 0.6318819690628784,
                  "feature_inter_percentile_range_2_magn_g": 0.9929466247558594,
                  "feature_inter_percentile_range_10_magn_g": 0.9186442341067504,
                  "feature_inter_percentile_range_25_magn_g": 0.5220851898193359,
                  "feature_kurtosis_magn_g": 0.5086429438541602,
                  "feature_linear_fit_slope_magn_g": -0.04286909081049682,
                  "feature_linear_fit_slope_sigma_magn_g": 0.007170496308801001,
                  "feature_linear_fit_reduced_chi2_magn_g": 3.944731401504837,
                  "feature_linear_trend_magn_g": -0.04926696578928191,
                  "feature_linear_trend_sigma_magn_g": 0.014325957190305598,
                  "feature_magnitude_percentage_ratio_40_5_magn_g": 0.15793874343909514,
                  "feature_magnitude_percentage_ratio_20_5_magn_g": 0.6632645325489513,
                  "feature_maximum_slope_magn_g": 0.19257662811473367,
                  "feature_mean_magn_g": 19.040957042149135,
                  "feature_median_absolute_deviation_magn_g": 0.06338119506835938,
                  "feature_percent_amplitude_magn_g": 0.9295654296875,
                  "feature_percent_difference_magnitude_percentile_5_magn_g": 0.05277543176373589,
                  "feature_percent_difference_magnitude_percentile_10_magn_g": 0.04882623585549797,
                  "feature_median_buffer_range_percentage_10_magn_g": 0.42857142857142855,
                  "feature_median_buffer_range_percentage_20_magn_g": 0.5714285714285714,
                  "feature_period_0_magn_g": 28.416087999939915,
                  "feature_period_s_to_n_0_magn_g": 3.2097690245910626,
                  "feature_period_1_magn_g": 6.216019249986856,
                  "feature_period_s_to_n_1_magn_g": 1.5694631400112595,
                  "feature_period_2_magn_g": 1.9694318415799943,
                  "feature_period_s_to_n_2_magn_g": 1.002651302726573,
                  "feature_period_3_magn_g": 2.0297205714242796,
                  "feature_period_s_to_n_3_magn_g": 0.9906025728142175,
                  "feature_period_4_magn_g": 2.6521682133277253,
                  "feature_period_s_to_n_4_magn_g": 0.7579493891399673,
                  "feature_periodogram_amplitude_magn_g": 1.2170992304016284,
                  "feature_periodogram_beyond_2_std_magn_g": 0.0546875,
                  "feature_periodogram_beyond_3_std_magn_g": 0.015625,
                  "feature_periodogram_standard_deviation_magn_g": 0.557789567707368,
                  "feature_chi2_magn_g": 9.244430647983117,
                  "feature_skew_magn_g": 1.3155722500191147,
                  "feature_standard_deviation_magn_g": 0.38538291905766153,
                  "feature_stetson_k_magn_g": 0.8333281628494618,
                  "feature_weighted_mean_magn_g": 18.93092611692064,
                  "feature_anderson_darling_normal_flux_g": 0.6550989457284369,
                  "feature_cusum_flux_g": 0.40317860290610325,
                  "feature_eta_e_flux_g": 0.5045000455592914,
                  "feature_excess_variance_flux_g": 0.07832520906918351,
                  "feature_kurtosis_flux_g": -0.5088382569098107,
                  "feature_mean_variance_flux_g": 0.29664272328799474,
                  "feature_chi2_flux_g": 13.11543926762407,
                  "feature_skew_flux_g": -1.0592793738347128,
                  "feature_stetson_k_flux_g": 0.904335301328353
                },
                "htm16": 59271501911,
                "catalogs": [
                  "nyu_valueadded_gals",
                  "allwise",
                  "2mass_psc",
                  "sdss_gals",
                  "bright_guide_star_cat",
                  "ned",
                  "2mass_xsc",
                  "gaia_dr2",
                  "french_post_starburst_gals"
                ],
                "tags": [
                  "extragalactic",
                  "nuclear_transient",
                  "lc_feature_extractor"
                ],
                "ra": 207.8682535299866
              },
              "relationships": {
                "alerts": {
                  "links": {
                    "related": "http://api.antares.noirlab.edu/v1/loci/ANT2018akftg/alerts"
                  }
                },
                "locus": {
                  "links": {
                    "related": "http://api.antares.noirlab.edu/v1/loci/ANT2018akftg"
                  }
                }
              }
            }
          ],
          "links": {
            "self": "http://api.antares.noirlab.edu/v1/loci?sort=-properties.newest_alert_observation_time&elasticsearch_query%5Blocus_listing%5D=%7B%22query%22%3A+%7B%22bool%22%3A+%7B%22filter%22%3A+%7B%22term%22%3A+%7B%22properties.ztf_object_id%22%3A+%22ZTF18aaviokz%22%7D%7D%7D%7D%7D"
          },
          "meta": {
            "count": 1,
            "aggregations": {
              "min_num_measurements": {
                "value": 11.0
              },
              "max_num_measurements": {
                "value": 11.0
              },
              "catalogs": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                  {
                    "key": "2mass_psc",
                    "doc_count": 1
                  },
                  {
                    "key": "2mass_xsc",
                    "doc_count": 1
                  },
                  {
                    "key": "allwise",
                    "doc_count": 1
                  },
                  {
                    "key": "bright_guide_star_cat",
                    "doc_count": 1
                  },
                  {
                    "key": "french_post_starburst_gals",
                    "doc_count": 1
                  },
                  {
                    "key": "gaia_dr2",
                    "doc_count": 1
                  },
                  {
                    "key": "ned",
                    "doc_count": 1
                  },
                  {
                    "key": "nyu_valueadded_gals",
                    "doc_count": 1
                  },
                  {
                    "key": "sdss_gals",
                    "doc_count": 1
                  }
                ]
              },
              "tags": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                  {
                    "key": "extragalactic",
                    "doc_count": 1
                  },
                  {
                    "key": "lc_feature_extractor",
                    "doc_count": 1
                  },
                  {
                    "key": "nuclear_transient",
                    "doc_count": 1
                  }
                ]
              }
            }
          }
        }
      }
    }
