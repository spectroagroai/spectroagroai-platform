import { Link } from 'react-router-dom'

export default function ProjectInfoPage() {
  return (
    <div className="min-h-screen overflow-y-auto bg-[#0b1220] text-slate-200">
      <div className="mx-auto max-w-6xl px-6 py-16 text-left">
        <header className="mb-16 border-b border-slate-800 pb-10">
          <div className="mb-3 text-sm uppercase tracking-[0.35em] text-cyan-300">
            SpectroAgro Fusion AI INDEX
          </div>

          <h1 className="mb-6 text-5xl font-bold text-white">
            SAFI — Digital Soil Laboratory and Land Suitability Platform
          </h1>

          <p className="max-w-5xl text-lg leading-8 text-slate-300">
            SpectroAgro Fusion AI (SAFI) is a Geo-AI based Digital Soil Laboratory
            designed to estimate key soil laboratory properties and derive a
            Land Suitability Index (LSI) directly from geographic coordinates.
            The platform combines remote sensing, climate, terrain, ecological,
            and soil-context variables to estimate agricultural potential in
            locations where no field laboratory measurements are available.
          </p>

          <p className="mt-4 max-w-5xl text-lg leading-8 text-slate-300">
            SAFI is intended for exploratory agricultural assessment, land
            comparison, sustainability studies, and early-stage planning. It is
            not intended to replace laboratory analysis or regulatory soil
            surveys.
          </p>

          <div className="mt-8">
            <Link
              to="/app"
              className="rounded-xl bg-cyan-500 px-6 py-3 font-medium text-black transition hover:bg-cyan-400"
            >
              Open SAFI Platform
            </Link>
          </div>
        </header>

        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            1. Project Objective
          </h2>

          <p className="leading-8 text-slate-300">
            The objective of SAFI is to create a scientifically defensible
            inference system capable of predicting soil properties in places
            where direct measurements do not exist. Instead of relying on a
            single variable, the system integrates many environmental signals
            related to soil formation and land productivity.
          </p>

          <p className="mt-4 leading-8 text-slate-300">
            The final output is a continuous Land Suitability Index ranging from
            0 to 1, representing the relative agricultural suitability of the
            selected location.
          </p>
        </section>

        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            2. Reference Dataset
          </h2>

          <p className="leading-8 text-slate-300">
            SAFI was developed using the unified dataset
            <span className="font-mono text-cyan-300"> safi_v1_universe.csv</span>,
            which contains approximately 4,416 georeferenced soil observations
            and around 159 environmental variables.
          </p>

          <div className="mt-6 overflow-hidden rounded-xl border border-slate-700">
            <table className="w-full border-collapse text-left text-slate-300">
              <thead className="bg-slate-800 text-white">
                <tr>
                  <th className="w-1/3 px-4 py-3 align-top">Dataset Component</th>
                  <th className="w-1/3 px-4 py-3 align-top">Description</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">Soil Points</td>
                  <td className="w-1/3 px-4 py-3 align-top">~4416 georeferenced observations</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">Environmental Features</td>
                  <td className="w-1/3 px-4 py-3 align-top">~159 remote sensing, climate, terrain, and ecological variables</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">Target Variables</td>
                  <td className="w-1/3 px-4 py-3 align-top">CECPH7, TOTC, ORGC, BDFIOD and derived ORGM</td>
                </tr>
              </tbody>
            </table>
          </div>
            <p className="mt-4 text-justify leading-8 text-slate-300">
            The environmental variables used in SAFI represent long-term conditions
            covering the period from 2001 to 2017. All remote sensing, climate,
            hydrological, and ecological features were aggregated across this time span
            in order to describe the stable environmental context of each soil sample and
            reduce short-term variability.
            </p>
        </section>

        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            3. Environmental Data Sources
          </h2>

          <div className="overflow-hidden rounded-xl border border-slate-700">
            <table className="w-full border-collapse text-left text-slate-300">
              <thead className="bg-slate-800 text-white">
                <tr>
                  <th className="w-1/3 px-4 py-3 align-top">Source</th>
                  <th className="w-1/3 px-4 py-3 align-top">Variables</th>
                  <th className="w-1/3 px-4 py-3 align-top">Purpose</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">WoSIS</td>
                  <td className="w-1/3 px-4 py-3 align-top">Measured soil laboratory observations</td>
                  <td className="w-1/3 px-4 py-3 align-top">Primary source for training and validation targets</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">ERA5</td>
                  <td className="w-1/3 px-4 py-3 align-top">Temperature, precipitation, wind, evaporation, radiation, soil moisture</td>
                  <td className="w-1/3 px-4 py-3 align-top">Long-term climate and energy balance</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">CHELSA</td>
                  <td className="w-1/3 px-4 py-3 align-top">Bioclimatic variables</td>
                  <td className="w-1/3 px-4 py-3 align-top">Captures climatic gradients and seasonality</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">GLDAS</td>
                  <td className="w-1/3 px-4 py-3 align-top">Root-zone and multi-depth soil moisture</td>
                  <td className="w-1/3 px-4 py-3 align-top">Hydrological context and water availability</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">MODIS / Landsat</td>
                  <td className="w-1/3 px-4 py-3 align-top">NDVI, NDMI, SAVI, NPP, burn frequency</td>
                  <td className="w-1/3 px-4 py-3 align-top">Vegetation productivity and land-surface response</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">Digital Elevation Models</td>
                  <td className="w-1/3 px-4 py-3 align-top">Elevation, aspect, curvature, TPI</td>
                  <td className="w-1/3 px-4 py-3 align-top">Topographic controls on soil formation</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            4. Processing Workflow
          </h2>

          <ol className="list-decimal space-y-4 pl-6 leading-8 text-slate-300">
            <li>The user selects a location on the map.</li>
            <li>SAFI extracts the nearest environmental feature vector from the reference dataset.</li>
            <li>The feature vector is validated against the SAFI schema.</li>
            <li>The inference engine predicts the main soil variables.</li>
            <li>Uncertainty intervals are calculated for every variable.</li>
            <li>The Land Suitability Index is derived from the predicted variables.</li>
            <li>The system reports results, confidence, and possible warnings.</li>
          </ol>
        </section>

        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            5. Model Training and Validation
          </h2>

          <p className="leading-8 text-slate-300">
            All SAFI models were trained using strict spatial cross-validation
            rather than random train-test splits. The system uses hierarchical
            spatial blocking and GroupKFold validation to ensure that nearby
            points are not simultaneously used for training and testing.
          </p>

          <div className="mt-6 overflow-hidden rounded-xl border border-slate-700">
            <table className="w-full border-collapse text-left text-slate-300">
              <thead className="bg-slate-800 text-white">
                <tr>
                  <th className="w-1/3 px-4 py-3 align-top">Target</th>
                  <th className="w-1/3 px-4 py-3 align-top">Model</th>
                  <th className="w-1/3 px-4 py-3 align-top">Validation Result</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">CECPH7</td>
                  <td className="w-1/3 px-4 py-3 align-top">Gradient Boosting Quantile Regression + Conformal Calibration</td>
                  <td className="w-1/3 px-4 py-3 align-top">RMSE ≈ 10.9, MAE ≈ 5.6, Spearman ≈ 0.81</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">TOTC</td>
                  <td className="w-1/3 px-4 py-3 align-top">Regime-Adaptive Quantile Regression</td>
                  <td className="w-1/3 px-4 py-3 align-top">RMSE ≈ 65–70, Spearman ≈ 0.75–0.80</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">ORGC</td>
                  <td className="w-1/3 px-4 py-3 align-top">LightGBM + Mondrian CV+ Intervals</td>
                  <td className="w-1/3 px-4 py-3 align-top">RMSE ≈ 35, Spearman ≈ 0.72</td>
                </tr>
                <tr className="border-t border-slate-700">
                  <td className="w-1/3 px-4 py-3 align-top">BDFIOD</td>
                  <td className="w-1/3 px-4 py-3 align-top">Bayesian Ridge + Residual Scale Model</td>
                  <td className="w-1/3 px-4 py-3 align-top">RMSE ≈ 0.28, Spearman ≈ 0.62</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p className="mt-6 leading-8 text-slate-300">
            Prediction intervals were calibrated to provide approximately 80%
            spatial coverage, ensuring that SAFI communicates uncertainty rather
            than only a single deterministic value.
          </p>
        </section>

        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            6. Predicted Soil Variables
          </h2>

          <div className="overflow-hidden rounded-xl border border-slate-700">
            <table className="w-full border-collapse text-left text-slate-300">
              <thead className="bg-slate-800 text-white">
                <tr>
                  <th className="w-1/3 px-4 py-3 align-top">Variable</th>
                  <th className="w-1/3 px-4 py-3 align-top">Meaning</th>
                  <th className="w-1/3 px-4 py-3 align-top">Function in SAFI</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">CECPH7</td><td className="w-1/3 px-4 py-3 align-top">Cation exchange capacity at pH 7</td><td className="w-1/3 px-4 py-3 align-top">Main positive soil fertility driver</td></tr>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">TOTC</td><td className="w-1/3 px-4 py-3 align-top">Total organic carbon</td><td className="w-1/3 px-4 py-3 align-top">Represents overall soil fertility</td></tr>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">ORGC</td><td className="w-1/3 px-4 py-3 align-top">Organic carbon</td><td className="w-1/3 px-4 py-3 align-top">Supporting carbon modifier</td></tr>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">BDFIOD</td><td className="w-1/3 px-4 py-3 align-top">Bulk density of fine earth</td><td className="w-1/3 px-4 py-3 align-top">Acts as a limiting physical factor</td></tr>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">ORGM</td><td className="w-1/3 px-4 py-3 align-top">Derived soil organic matter</td><td className="w-1/3 px-4 py-3 align-top">Diagnostic only</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            7. Land Suitability Index (LSI)
          </h2>

          <p className="leading-8 text-slate-300">
            SAFI converts each predicted soil property into a percentile score
            relative to the reference population. These percentile scores are
            then combined using a limiting-factor logic.
          </p>

          <div className="mt-6 rounded-xl border border-slate-700 bg-slate-950 p-6 font-mono text-cyan-300">
            PositiveScore = mean(Percentile(CECPH7), Percentile(TOTC))
            <br />
            ConstraintFactor = sqrt(Percentile(ORGC) × (1 - Percentile(BDFIOD)))
            <br />
            LSI = PositiveScore × ConstraintFactor
          </div>

          <p className="mt-6 leading-8 text-slate-300">
            High CECPH7 and TOTC increase suitability because they indicate
            better nutrient retention and higher fertility. High BDFIOD reduces
            the final score because dense soil limits root growth and water
            movement.
          </p>

          <div className="mt-6 overflow-hidden rounded-xl border border-slate-700">
            <table className="w-full border-collapse text-left text-slate-300">
              <thead className="bg-slate-800 text-white">
                <tr>
                  <th className="w-1/3 px-4 py-3 align-top">LSI Range</th>
                  <th className="w-1/3 px-4 py-3 align-top">Interpretation</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">0.00 – 0.20</td><td className="w-1/3 px-4 py-3 align-top">Very low suitability</td></tr>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">0.20 – 0.40</td><td className="w-1/3 px-4 py-3 align-top">Low suitability</td></tr>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">0.40 – 0.60</td><td className="w-1/3 px-4 py-3 align-top">Moderate suitability</td></tr>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">0.60 – 0.80</td><td className="w-1/3 px-4 py-3 align-top">High suitability</td></tr>
                <tr className="border-t border-slate-700"><td className="w-1/3 px-4 py-3 align-top">0.80 – 1.00</td><td className="w-1/3 px-4 py-3 align-top">Excellent suitability</td></tr>
              </tbody>
            </table>
          </div>

          <ul className="mt-6 list-disc space-y-2 pl-6 text-slate-300">
            <li>Conservative LSI: based on lower uncertainty bounds.</li>
            <li>Expected LSI: based on central predictions.</li>
            <li>Opportunity LSI: based on upper uncertainty bounds.</li>
          </ul>
        </section>
        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
        <h2 className="mb-5 text-3xl font-semibold text-white">
            8. Future Development
        </h2>

        <p className="text-justify leading-8 text-slate-300">
            The current SAFI version operates in an offline mode using precomputed
            environmental features extracted from the reference dataset.
        </p>

        <p className="mt-4 text-justify leading-8 text-slate-300">
            The next development stage currently in progress is the transition toward a
            full dynamic inference system. In the future, when a user selects a point
            on the map, SAFI will automatically retrieve the complete environmental
            context of that location in real time.
        </p>

        <p className="mt-4 text-justify leading-8 text-slate-300">
            This future workflow will extract all relevant variables directly from
            their original sources, including:
        </p>

        <ul className="mt-4 list-disc space-y-3 pl-6 text-justify text-slate-300">
            <li>Current and historical climate variables from ERA5 and CHELSA</li>
            <li>Satellite remote sensing indicators such as NDVI, NDMI and SAVI</li>
            <li>Soil moisture and hydrological indicators from GLDAS</li>
            <li>Topographic and terrain characteristics from digital elevation models</li>
            <li>Land cover, lithology and ecological variables</li>
        </ul>

        <p className="mt-4 text-justify leading-8 text-slate-300">
            These dynamically extracted variables will then be passed directly into the
            existing SAFI prediction models. This approach is expected to produce more
            accurate, location-specific and up-to-date soil predictions and Land
            Suitability Index estimates than the current nearest-neighbor method.
        </p>
        </section>
        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            9. Scientific Limitations
          </h2>

          <ul className="list-disc space-y-3 pl-6 leading-8 text-slate-300">
            <li>The current version uses nearest-neighbor lookup from the reference dataset.</li>
            <li>The platform does not yet use live raster layers or real-time satellite data.</li>
            <li>Prediction uncertainty increases in rare or unsupported environments.</li>
            <li>Locations outside the environmental domain of the training dataset may produce lower-confidence results.</li>
            <li>SAFI is intended for screening and comparison, not as a replacement for field sampling and laboratory measurements.</li>
          </ul>
        </section>
        <section className="mb-12 rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            10. Partnerships, Funding and Collaboration
          </h2>

          <p className="leading-8 text-slate-300">
            SAFI is currently under active development. Universities, companies,
            research institutes, government agencies, agricultural organizations, and
            potential investors are welcome to collaborate in order to support model
            improvement, provide additional soil datasets, develop new features, or
            establish scientific and commercial partnerships.
          </p>

          <div className="mt-6 rounded-xl border border-slate-700 bg-slate-950/60 p-5">
            <div className="grid gap-4 md:grid-cols-[180px_1fr] text-slate-300">
              <div className="font-semibold text-white">Contact Email</div>
              <div>
                <a
                  href="mailto:founder@spectroagroai.world"
                  className="text-cyan-300 hover:text-cyan-200"
                >
                  founder@spectroagroai.world
                </a>
              </div>

              <div className="font-semibold text-white">Project Website</div>
              <div>
                <a
                  href="https://spectroagroai.world/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-cyan-300 hover:text-cyan-200"
                >
                  https://spectroagroai.world/
                </a>
              </div>
            </div>
          </div>
        </section>
        <section className="rounded-2xl border border-slate-800 bg-slate-900/50 p-8">
          <h2 className="mb-5 text-3xl font-semibold text-white">
            11. Project Founder and Origin
          </h2>

          <p className="text-justify leading-8 text-slate-300">
            SAFI was developed by Hussein Hadi Abbas, a Surveying Engineer graduated from
            the Middle Technical University, Iraq, with a research background in remote
            sensing, GIS, and AI-driven geospatial analysis. He also holds a Master’s
            degree in Map (Geomatics) Engineering from Erciyes University, Türkiye.
          </p>

          <p className="mt-4 text-justify leading-8 text-slate-300">
            The idea behind SAFI began in 2022 during a discussion about a privately
            owned agricultural farm. The central question was whether it would be
            possible to infer the essential characteristics of land without relying
            entirely on expensive and time-consuming laboratory testing.
          </p>

          <p className="mt-4 text-justify leading-8 text-slate-300">
            The discussion gradually evolved into a broader scientific problem: if a
            person intends to purchase or cultivate a piece of land, what are the minimum
            indicators required to determine whether that land is suitable for
            agriculture? Could soil laboratory properties be estimated from satellite
            observations, climate, terrain, and environmental context? And could these
            estimates be transformed into a simple, interpretable indicator expressing
            the overall suitability of the land?
          </p>

          <p className="mt-4 text-justify leading-8 text-slate-300">
            From these questions, SAFI emerged as an attempt to create a Digital Soil
            Laboratory and a Land Suitability Index capable of translating complex
            environmental information into practical guidance for agricultural planning
            and decision-making.
          </p>
        </section>
      </div>
    </div>
  )
}