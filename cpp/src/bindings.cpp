/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */


#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include "world.hpp"
#include "entity.hpp"
#include "filter.hpp"

namespace py = pybind11;
using namespace pyflecs;

void wrap_entity_set(entity* e, entity*c,
    py::array_t<uint8_t, py::array::c_style | py::array::forcecast> data)
{
    py::buffer_info info = data.request();
    e->set(*c, data.nbytes(), info.ptr);
}

py::array_t<uint8_t> wrap_entity_get(entity* e, entity* c)
{
    auto ptr = reinterpret_cast<const uint8_t*>(e->get(*c));
    // Must pass a dummy owner such that pybind will return the data without
    // modification: https://github.com/pybind/pybind11/issues/323
    py::str dummy;
    return py::array_t<uint8_t>(c->size(), ptr, dummy);
}

void wrap_entity_set_pair(entity* e, entity* c, entity* other,
    py::array_t<uint8_t, py::array::c_style | py::array::forcecast> data)
{
    py::buffer_info info = data.request();
    e->set_pair(*c, *other, data.nbytes(), info.ptr);
}

py::array_t<uint8_t> wrap_iter_term(pyflecs::iter *iter, entity& e,
    int32_t idx)
{
    auto result = reinterpret_cast<const uint8_t*>(
        iter->get_term_data(e, idx));
    size_t count = iter->count();
    if (!iter->term_owned(idx))
        count = 1;
    uint32_t size = count * iter->term_size(idx);
    if (result == nullptr)
        size = 0;

    py::str dummy; // See note above about ownership
    return py::array_t<uint8_t>(size, result, dummy);
}

void wrap_world_set(world* w, entity* c,
    py::array_t<uint8_t, py::array::c_style | py::array::forcecast> data)
{
    // The world's entity set for a singleton is just setting the entity
    // to the component.
    if (!c->has(*c))
        c->add(*c);
    wrap_entity_set(c, c, data);
}

py::array_t<uint8_t> wrap_world_get(world* w, entity* c)
{
    return wrap_entity_get(c, c);
}

PYBIND11_MODULE(_flecs, m) {
    m.doc() = "Python bindings to flecs library";

    py::enum_<ecs_inout_kind_t>(m, "ecs_inout_kind_t")
        .value("Default", ecs_inout_kind_t::EcsInOutDefault)
        .value("Filter", ecs_inout_kind_t::EcsInOutFilter)
        .value("InOut", ecs_inout_kind_t::EcsInOut)
        .value("In", ecs_inout_kind_t::EcsIn)
        .value("Out", ecs_inout_kind_t::EcsOut)
        .export_values();

    py::class_<ecs_term_t>(m, "ecs_term_t")
        .def(py::init<>())
        .def_readwrite("id", &ecs_term_t::id)
        .def_readwrite("inout", &ecs_term_t::inout)
        ;

    py::class_<pyflecs::type>(m, "type")
        .def("string", &pyflecs::type::string)
        .def("length", &pyflecs::type::length)
        ;

    py::class_<pyflecs::id>(m, "id")
        .def("is_pair", &pyflecs::id::is_pair)
        .def("object", &pyflecs::id::object)
        .def("relation", &pyflecs::id::relation)
        .def("as_entity", &pyflecs::id::as_entity)
        ;

    py::class_<entity>(m, "entity")
        .def("is_alive", &entity::is_alive)
        .def("destruct", &entity::destruct)
        .def("name", &entity::name)
        .def("add", &entity::add)
        .def("set", &wrap_entity_set)
        .def("get", &wrap_entity_get, py::return_value_policy::reference)
        .def("remove", &entity::remove)
        .def("has", &entity::has)
        .def("raw", &entity::raw)

        // Pairs
        .def("add_pair", &entity::add_pair)
        .def("remove_pair", &entity::remove_pair)
        .def("has_pair", &entity::has_pair)
        .def("set_pair", &wrap_entity_set_pair)

        // Hierarchies
        .def("path", &entity::path)
        .def("add_child", &entity::add_child)
        .def("lookup", &entity::lookup)
        
        // Instancing
        .def("is_a", &entity::is_a)

        // Type
        .def("type", &entity::type)
        ;

    py::class_<pyflecs::iter>(m, "iter")
        .def("next", &iter::next)
        .def("count", &iter::count)
        .def("term_count", &iter::term_count)
        .def("term", &iter::term)
        .def("get_entity", &iter::get_entity)
        .def("data", &wrap_iter_term,
            py::return_value_policy::reference)
        ;

    py::class_<filter>(m, "filter")
        .def("iter", &filter::iter)
        .def("term_count", &filter::term_count)
        .def("terms", &filter::terms)
        ;

    py::class_<query>(m, "query")
        .def("iter", &query::iter)
        .def("term_count", &query::term_count)
        .def("terms", &query::terms)
        ;

    py::class_<world>(m, "world")
        .def(py::init<>())
        .def("entity", py::overload_cast<>(&world::entity))
        .def("entity", py::overload_cast<std::string>(&world::entity))
        .def("entity", py::overload_cast<pyflecs::entity&>(&world::entity))
        .def("lookup", &world::lookup)
        .def("lookup_path", &world::lookup_path)
        .def("lookup_by_id", &world::lookup_by_id)
        .def("component", &world::component)
        .def("create_filter", &world::create_filter)
        .def("create_query", &world::create_query)
        .def("create_term_iter", &world::create_term_iter)
        .def("set", &wrap_world_set)
        .def("get", &wrap_world_get, py::return_value_policy::reference)

        //  function
        .def("pair", [](world* w, entity* e, entity* other) {
                return pyflecs::entity(w->raw(), ecs_pair(e->raw(), other->raw()));
            })

        // Hooks to special entities
        .def("EcsPrefab", [](world* w) {
            return pyflecs::entity(w->raw(), EcsPrefab);
            })
        .def("EcsIsA", [](world* w) {
                return pyflecs::entity(w->raw(), EcsIsA);
            })
        .def("EcsChildOf", [](world* w) {
                return pyflecs::entity(w->raw(), EcsChildOf);
            })
        ;

}