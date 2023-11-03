import React from 'react';
import ReactDOM from 'react-dom';
import {
	ReactiveBase,
	DataSearch,
	MultiList,
	SingleRange,
	ReactiveList,
	ResultCard,
  RangeSlider,
  SearchBox,
  MultiDataList,
  DateRange,
  SelectedFilters,  
} from '@appbaseio/reactivesearch';
import './index.css';

class Main extends React.Component {
  render() {
    return (
      <ReactiveBase
        app="hotels" // Nombre de tu aplicación de Elasticsearch
        url="http://localhost:9200" // URL de tu instancia de Elasticsearch
      >
        <div style={{ display: 'flex', flexDirection: 'row' }}>
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              width: '30%',
              margin: '10px',
            }}
          >
            <div>
              <MultiList
                componentId="authorsfilter"
                dataField="nombre"
                title="Filter by Authors"
                aggregationSize={5}
              />
            </div>
            <SingleRange
              componentId="ratingsfilter"
              dataField="categoria"
              title="Filtrar por categoría"
              data={[
                { start: 4, end: 5, label: '4 stars and up' },
                { start: 3, end: 5, label: '3 stars and up' },
              ]}
              defaultValue="4 stars and up"
            />
            <RangeSlider
              dataField="n_opiniones"
              componentId="opinion_range_slider"
              range={{
                start: 0,
                end: 10000,
              }}
              rangeLabels={{
                start: '0',
                end: '10 mil',
              }}
            />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', width: '66%' }}>
            <DataSearch
              componentId="searchbox"
              dataField={[
                {
                  field: 'nombre',
                  weight: 3,
                },
                {
                  field: 'localizacion',
                  weight: 1,
                },
                {
                  field: 'comunidad',
                  weight: 5,
                },
              ]}
              placeholder="Buscar hotel"
            />
            <ReactiveList
              componentId="results"
              dataField="_score"
              size={6}
              pagination={true}
              react={{
                and: ['searchbox', 'authorsfilter', 'ratingsfilter', 'opinion_range_slider'],
              }}
              loader={<div>Cargando...</div>}
              showResultStats={true}
              render={({ data }) => (
                <ReactiveList.ResultCardsWrapper>
                  {data.map((item) => (
                    <ResultCard key={item._id}>
                      <ResultCard.Image src={item.image} />
                      <ResultCard.Title
                        dangerouslySetInnerHTML={{
                          __html: item.nombre,
                        }}
                      />
                      <ResultCard.Description>
                        {item.comunidad + ' ' + '*'.repeat(item.puntuacion)}
                        {item.n_opiniones}
                      </ResultCard.Description>
                    </ResultCard>
                  ))}
                </ReactiveList.ResultCardsWrapper>
              )}
              renderResultStats={
                function(stats){
                    return (
                        `Mostrando ${stats.displayedResults} de un total de ${stats.numberOfResults} encontrados en ${stats.time} ms`
                    )
                }
            }
            />
          </div>
        </div>
      </ReactiveBase>
    );
  }
}

ReactDOM.render(<Main />, document.getElementById('root'));


