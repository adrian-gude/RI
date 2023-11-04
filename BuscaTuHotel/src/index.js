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
  RatingsFilter,
  MultiRange,
  MultiDropdownRange,
  MultiDropdownList,
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
            <MultiDropdownList
              componentId="comunidad_multidropselector"
              compoundClause="filter"
              dataField="comunidad.keyword"
              title="Comunidades"
              //size={100}
              sortBy="asc"
              showCount={true}
              placeholder="Comunidades"
              showFilter={true}  
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'precio_multiselector', 'puntuacion_slider', 'categoria_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }} 
            />
            <MultiRange
              componentId="precio_multiselector"
              compoundClause="filter"
              dataField="precio"
              data={[
                { start: 0, end: 50, label: '1 - 50 €' },
                { start: 50, end: 150, label: '50 - 150 €' },
                { start: 150, end: 500, label: '150 - 500 €' },
                { start: 500, label: '500 € o más' },
              ]}
              title="Precio"
              showCheckbox={true}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'precio_multiselector', 'puntuacion_slider', 'categoria_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }}
            />
            <RangeSlider
              componentId="puntuacion_slider"
              dataField="puntuacion"
              title="Puntuación"
              range={{
                start: 0.0,
                end: 5.0,
              }}
              rangeLabels={{
                start: '0',
                end: '5',
              }}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'precio_multiselector', 'puntuacion_slider', 'categoria_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }}
            />
            <RatingsFilter
              componentId="categoria_ratingselector"
              dataField="categoria"
              title="Categoría"
              data={[
                { start: 0, end: 5, label: 'Todos' },
                { start: 1, end: 5, label: '1 o más' },
                { start: 2, end: 5, label: '2 o más' },
                { start: 3, end: 5, label: '3 o más' },
                { start: 4, end: 5, label: '4 o más' },
                { start: 5, end: 5, label: '5' }
              ]}
              /*defaultValue={{
                start: 0,
                end: 5,
              }}*/
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'precio_multiselector', 'puntuacion_slider', 'categoria_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }}
            />
            <MultiDropdownList
              componentId="idiomas_multidropselector"
              compoundClause="filter"
              dataField="idiomas.keyword"
              title="Idiomas"
              //size={100}
              sortBy="count"
              showCount={true}
              placeholder="Idiomas"
              showFilter={true}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'precio_multiselector', 'puntuacion_slider', 'categoria_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }} 
            />
            <MultiDropdownList
              componentId="servicios_multidropselector"
              compoundClause="filter"
              dataField="servicios.keyword"
              title="Servicios"
              //size={100}
              sortBy="count"
              showCount={true}
              placeholder="Servicios"
              showFilter={true}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'precio_multiselector', 'puntuacion_slider', 'categoria_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
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
                }
              ]}
              placeholder="Buscar hotel"
              autosuggest={true}
              //enableRecentSuggestions={true}
              //enablePopularSuggestions={true}
              //enablePredictiveSuggestions={true}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'precio_multiselector', 'puntuacion_slider', 'categoria_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }}
            />
            <ReactiveList
              componentId="results"
              dataField="_score"
              size={6}
              //sortBy='desc'
              sortOptions={[ //TODO
                {
                  label: "Desc",
                  dataField: "_score",
                  sortBy: "desc"
                },
                {
                  label: "Asc",
                  dataField: "_score",
                  sortBy: "asc"
                }
              ]}
              defaultSortOption='Desc'
              stream={true}
              pagination={true}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'precio_multiselector', 'puntuacion_slider', 'categoria_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }}
              loader={<div>Cargando...</div>}
              showResultStats={true} //Mostrar estadísticas de resultados
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
                        {item.comunidad + ' ' + '*'.repeat(item.puntuacion)+'\n'}
                        {item.n_opiniones}
                      </ResultCard.Description>
                    </ResultCard>
                  ))}
                </ReactiveList.ResultCardsWrapper>
              )}
              renderResultStats={ //Definir estadísticas personalizadas de resultados
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


//TODO: (PENDIENTE)
/*
- Permitir elegir al usuario el nº de elementos por página a mostrar
- Mejorar el diseño de la página (estilo, colores, etc.)
- Intentar incluír un mapa con el nº de hoteles por comunidad
- Hacer el ordenacimiento del listado, actualmente no funciona
- Hacer que si pinchas en un hotel te lleve a su página web (haciendo uso del campo 'url)
*/



