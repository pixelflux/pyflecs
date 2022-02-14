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

#pragma once

#include "flecs.h"
#include <string>


namespace pyflecs {
    /**
     * Wraps the entity type. 
     */
    class type final {
    public:
        type(ecs_world_t* world, ecs_type_t t) : 
            mpWorld(world),
            mRaw(t)
        {

        }

        size_t length()
        {
            return ecs_vector_count(mRaw);
        }

        std::string string()
        {
            char* data = ecs_type_str(mpWorld, mRaw);
            std::string result(data);
            ecs_os_free(data);
            return result;
        }

    private:
        ecs_world_t* mpWorld;
        ecs_type_t mRaw;
    };

    /**
     * Approximates the flecs C++ class interface for an entity.
     */
    class entity final {
    public:
        entity(ecs_world_t* world, const ecs_entity_t e);
        ~entity();

        bool is_alive() const
        {
            return ecs_is_alive(mpWorld, mRaw);
        }

        void destruct()
        {
            ecs_delete(mpWorld, mRaw);
        }

        std::string name() const
        {
            const char* result = ecs_get_name(mpWorld, mRaw);
            if (result != nullptr)
                return std::string(result);
            else
                return std::string();
        }

        ecs_entity_t raw() const
        {
            return mRaw;
        }

        void add(entity& c)
        {
            ecs_add_id(mpWorld, mRaw, c.raw());
        }

        void set(entity& c, uint32_t size, const void* bytes)
        {
            ecs_set_id(mpWorld, mRaw, c.raw(), size, bytes);
        }

        const void* get(entity& c)
        {
            return ecs_get_id(mpWorld, mRaw, c.raw());
        }

        void remove(entity& c)
        {
            ecs_remove_id(mpWorld, mRaw, c.raw());
        }

        bool has(entity& c)
        {
            return ecs_has_id(mpWorld, mRaw, c.raw());
        }

        void add_pair(entity& c, entity& e)
        {
            ecs_add_pair(mpWorld, mRaw, c.raw(), e.raw());
        }

        void remove_pair(entity& c, entity& e)
        {
            ecs_remove_pair(mpWorld, mRaw, c.raw(), e.raw());
        }

        bool has_pair(entity& c, entity& e)
        {
            return ecs_has_id(mpWorld, mRaw, ecs_make_pair(c.raw(), e.raw()));
        }

        void set_pair(entity& c, entity& e, uint32_t size, const void* bytes)
        {
            ecs_set_id(mpWorld, mRaw, ecs_pair(c.raw(), e.raw()), size, bytes);
        }

        uint32_t size() const
        {
            const EcsComponent* c = ecs_get(mpWorld, mRaw, EcsComponent);
            return c->size;
        }

        std::string path() const
        {
            char* data = ecs_get_fullpath(mpWorld, mRaw);
            std::string result(data);
            ecs_os_free(data);
            return result;
        }

        void add_child(const entity& child)
        {
            ecs_add_pair(mpWorld, child.raw(), EcsChildOf, mRaw);
        }

        entity lookup(std::string name)
        {
            return entity(mpWorld, ecs_lookup_path(mpWorld, mRaw, 
                name.c_str()));
        }

        void is_a(const entity& base)
        {
            ecs_add_pair(mpWorld, mRaw, EcsIsA, base.raw());
        }

        pyflecs::type type()
        {
            // For now, return the string.
            return pyflecs::type(mpWorld, ecs_get_type(mpWorld, mRaw));
        }

    private:
        ecs_world_t* mpWorld;
        ecs_entity_t mRaw;

    };

    /**
 * Wraps the id which can be an entity or a pair.
 */
    class id final {
    public:
        id(ecs_world_t* world, ecs_id_t eid) :
            mpWorld(world),
            mRaw(eid)
        {

        }

        bool is_pair() const
        {
            return ecs_id_is_pair(mRaw);
        }

        pyflecs::entity relation() const
        {
            return pyflecs::entity(mpWorld, ecs_pair_relation(mpWorld, mRaw));
        }

        pyflecs::entity object() const
        {
            return pyflecs::entity(mpWorld, ecs_pair_object(mpWorld, mRaw));
        }

        pyflecs::entity as_entity() const
        {
            return pyflecs::entity(mpWorld, mRaw);
        }

    private:
        ecs_world_t* mpWorld;
        ecs_id_t mRaw;
    };
}
