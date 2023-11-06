import React from 'react';
import ReactDOM from 'react-dom';
import {
	ReactiveBase,
	DataSearch,
	ReactiveList,
	ResultCard,
  RangeSlider,
  RatingsFilter,
  MultiRange,
  MultiDropdownList,
} from '@appbaseio/reactivesearch';
import './index.css';

import StarIcon from '@mui/icons-material/Star';
import CircleIcon from '@mui/icons-material/Circle';
//import Rating from '@mui/material/Rating';

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
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider', 'puntuacion_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }} 
            />
            <RangeSlider
              componentId="precio_slider"
              dataField="precio"
              title="Precio"
              range={{
                start: 0,
                end: 1000,
              }}
              rangeLabels={{
                start: '0',
                end: '1000',
              }}
              showHistogram={true}
              showFilter={true}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider', 'puntuacion_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }}
            />
            <RatingsFilter
              componentId="puntuacion_ratingselector"
              dataField="puntuacion"
              title="Puntuacion"
              icon={<CircleIcon htmlColor="seagreen  " />}
              dimmedIcon={<CircleIcon htmlColor='grey'/>}
              data={[
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
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider', 'puntuacion_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }}
            />
            <MultiRange
              componentId="categoria_multiselector"
              compoundClause="filter"
              dataField="categoria"
              data={[
                //{ start: 1, end: 1, label: <StarIcon htmlColor="#F2B203"/> },
                { start: 1, end: 1, label: '1 estrella' },
                { start: 2, end: 2, label: '2 estrellas' },
                { start: 3, end: 3, label: '3 estrellas'  },
                { start: 4, end: 4, label: '4 estrellas'  },
                { start: 5, end: 5, label: '5 estrellas'  },
                //{ start: 5, end: 5, label: <Rating name="read-only" value={5} readOnly /> },
              ]}
              title="Categoria"
              showCheckbox={true}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider', 'puntuacion_ratingselector',
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
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider', 'puntuacion_ratingselector',
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
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider', 'puntuacion_ratingselector',
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
                }
              ]}
              placeholder="Buscar hotel"
              autosuggest={true}
              //enableRecentSuggestions={true}
              //enablePopularSuggestions={true}
              //enablePredictiveSuggestions={true}
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider', 'puntuacion_ratingselector',
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
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider', 'puntuacion_ratingselector',
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
- Definir visualización correcta de cada hotel del listado
- Intentar incluír un mapa con el nº de hoteles por comunidad
- Hacer el ordenacimiento del listado, actualmente no funciona
- Hacer que si pinchas en un hotel te lleve a su página web (haciendo uso del campo 'url)
- Verificar correcto funcionamiento de los componentes, en especial el buscador
- Comprobar que el diseño es responsive
*/



